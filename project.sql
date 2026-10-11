CREATE DATABASE IF NOT EXISTS project
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE project;

-- 1. Bảng tài khoản
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'ADMIN',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Bảng học viên
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone VARCHAR(20),
    date_of_birth DATE,
    address VARCHAR(255)
);

-- 3. Bảng giáo viên
CREATE TABLE IF NOT EXISTS teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone VARCHAR(20),
    specialty VARCHAR(120)
);

-- 4. Bảng khóa học
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL UNIQUE,
    description TEXT,
    duration_hours INT DEFAULT 0,
    tuition_fee FLOAT DEFAULT 0
);

-- 5. Bảng lớp học
CREATE TABLE IF NOT EXISTS classes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL UNIQUE,
    course_id INT NOT NULL,
    teacher_id INT NOT NULL,
    start_date DATE,
    end_date DATE,
    capacity INT DEFAULT 30,
    status VARCHAR(20) DEFAULT 'OPEN',

    CONSTRAINT fk_classes_course
        FOREIGN KEY (course_id) REFERENCES courses(id),

    CONSTRAINT fk_classes_teacher
        FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);

-- 6. Bảng đăng ký học
CREATE TABLE IF NOT EXISTS registrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    class_id INT NOT NULL,
    registered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'ACTIVE',

    CONSTRAINT uq_student_class
        UNIQUE (student_id, class_id),

    CONSTRAINT fk_registrations_student
        FOREIGN KEY (student_id) REFERENCES students(id),

    CONSTRAINT fk_registrations_class
        FOREIGN KEY (class_id) REFERENCES classes(id)
);

-- 7. Bảng kết quả học tập
CREATE TABLE IF NOT EXISTS results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    registration_id INT NOT NULL UNIQUE,
    score FLOAT,
    grade VARCHAR(20),
    comment TEXT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_results_registration
        FOREIGN KEY (registration_id) REFERENCES registrations(id)
);
