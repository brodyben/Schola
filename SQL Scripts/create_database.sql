drop database if exists `schola`;
create database `schola`;
use `schola`;

create table `user` (
  `username` varchar(10) primary key,
  `password` varchar(10) not null
);

create table `tutor` (
  `id` int primary key auto_increment,
  `name` varchar(30) not null,
  `login` varchar(10) not null unique,
  constraint `tutor_login_fk`
    foreign key (`login`) references `user` (`username`)
    on delete cascade on update cascade
);

create table `teacher` (
  `id` int primary key auto_increment,
  `name` varchar(30) not null,
  `login` varchar(10) not null unique,
  `department` varchar(30) not null,
  constraint `teacher_login_fk`
    foreign key (`login`) references `user` (`username`)
    on delete cascade on update cascade
);

create table `course` (
  `id` int primary key auto_increment,
  `name` varchar(50) not null,
  `term` enum('Fall','Spring','Summer 1','Summer 2') not null,
  `year` year(4) not null,
  `location` varchar(40) not null,
  `teacher_id` int not null,
  `weekday` set('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday') not null,
  `start_time` time not null,
  `end_time` time not null,
  constraint `teacher_fk`
    foreign key (`teacher_id`) references `teacher` (`id`)
    on delete cascade on update cascade
);

CREATE TABLE `office_hours` (
  `id` int primary key auto_increment,
  `location` varchar(40) not null,
  `weekday` enum('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday') not null,
  `start_time` time not null,
  `end_time` time not null,
  `tutor_id` int not null,
  `course_id` int not null,
  constraint `tutor_fk`
    foreign key (`tutor_id`) references `tutor` (`id`)
    on delete cascade on update cascade,
  constraint `course_fk`
    foreign key (`course_id`) references `course` (`id`)
    on delete cascade on update cascade
);
