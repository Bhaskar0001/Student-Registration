from django.db import connection

THRESHOLD_DAYS = 7


def fetch_dashboard_rows(limit=200, status=None):
    """
    Raw SQL for SQLite (dev). Uses Django-style %s placeholders (important).
    status can be: None / "ACTIVE" / "AT_RISK"
    """
    sql = """
    SELECT *
    FROM (
        SELECT
          id, student_uid, full_name, class_grade, last_login_at,
          CASE
            WHEN last_login_at IS NULL THEN 9999
            ELSE CAST((julianday('now') - julianday(last_login_at)) AS INTEGER)
          END AS inactivity_days,
          CASE
            WHEN last_login_at IS NULL THEN 'AT_RISK'
            WHEN (julianday('now') - julianday(last_login_at)) > %s THEN 'AT_RISK'
            ELSE 'ACTIVE'
          END AS engagement_status
        FROM students_student
    ) t
    """

    params = [THRESHOLD_DAYS]

    if status in ("ACTIVE", "AT_RISK"):
        sql += " WHERE engagement_status = %s "
        params.append(status)

    sql += " ORDER BY inactivity_days DESC, full_name ASC LIMIT %s; "
    params.append(limit)

    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        cols = [c[0] for c in cursor.description]
        return [dict(zip(cols, row)) for row in cursor.fetchall()]


def fetch_dashboard_counts():
    sql_total = "SELECT COUNT(*) FROM students_student;"
    sql_at_risk = """
    SELECT COUNT(*)
    FROM students_student
    WHERE last_login_at IS NULL
       OR (julianday('now') - julianday(last_login_at)) > %s;
    """

    with connection.cursor() as cursor:
        cursor.execute(sql_total)
        total = cursor.fetchone()[0]

        cursor.execute(sql_at_risk, [THRESHOLD_DAYS])
        at_risk = cursor.fetchone()[0]

    return {
        "total": total,
        "at_risk": at_risk,
        "active": total - at_risk,
    }
