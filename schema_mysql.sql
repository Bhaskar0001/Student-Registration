-- schema.sql (MySQL 8+)
-- Creates tables for: students, parents, parent-student link, audit logs

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- =========================
-- STUDENTS
-- =========================
DROP TABLE IF EXISTS students_student;

CREATE TABLE students_student (
  id BIGINT NOT NULL AUTO_INCREMENT,
  student_uid VARCHAR(16) NOT NULL UNIQUE,
  full_name VARCHAR(120) NOT NULL,
  class_grade VARCHAR(20) NOT NULL,

  email_enc LONGBLOB NOT NULL,
  mobile_enc LONGBLOB NOT NULL,

  email_hash BINARY(32) NOT NULL UNIQUE,
  mobile_hash BINARY(32) NOT NULL UNIQUE,

  last_login_at DATETIME(6) NULL,

  created_at DATETIME(6) NOT NULL,
  updated_at DATETIME(6) NOT NULL,

  PRIMARY KEY (id),
  INDEX idx_students_last_login_at (last_login_at),
  INDEX idx_students_full_name (full_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =========================
-- PARENTS
-- (NOTE: uses auth_user from Django)
-- =========================
DROP TABLE IF EXISTS parents_parent;

CREATE TABLE parents_parent (
  id BIGINT NOT NULL AUTO_INCREMENT,
  user_id INT NOT NULL UNIQUE,
  full_name VARCHAR(120) NOT NULL,
  created_at DATETIME(6) NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_parents_user FOREIGN KEY (user_id)
    REFERENCES auth_user(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =========================
-- STUDENT ↔ PARENT LINK
-- =========================
DROP TABLE IF EXISTS parents_studentparent;

CREATE TABLE parents_studentparent (
  id BIGINT NOT NULL AUTO_INCREMENT,
  student_id BIGINT NOT NULL,
  parent_id BIGINT NOT NULL,
  relationship VARCHAR(30) NOT NULL DEFAULT 'PARENT',
  created_at DATETIME(6) NOT NULL,

  PRIMARY KEY (id),
  UNIQUE KEY uq_student_parent (student_id, parent_id),

  CONSTRAINT fk_sp_student FOREIGN KEY (student_id)
    REFERENCES students_student(id) ON DELETE CASCADE,
  CONSTRAINT fk_sp_parent FOREIGN KEY (parent_id)
    REFERENCES parents_parent(id) ON DELETE CASCADE,

  INDEX idx_sp_student (student_id),
  INDEX idx_sp_parent (parent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =========================
-- AUDIT LOGS
-- =========================
DROP TABLE IF EXISTS audit_studentauditlog;

CREATE TABLE audit_studentauditlog (
  id BIGINT NOT NULL AUTO_INCREMENT,
  student_id BIGINT NOT NULL,
  field_name VARCHAR(64) NOT NULL,
  old_value LONGTEXT NULL,
  new_value LONGTEXT NULL,
  changed_by VARCHAR(128) NOT NULL,
  changed_at DATETIME(6) NOT NULL,

  PRIMARY KEY (id),
  INDEX idx_audit_student (student_id),
  INDEX idx_audit_changed_at (changed_at),

  CONSTRAINT fk_audit_student FOREIGN KEY (student_id)
    REFERENCES students_student(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;
