use `schola`;

insert into `user` (`username`, `password`) values
('bencla', 'password'),
('joesmi', 'password'),
('jimjoh', 'password'),
('jonste', 'password'),
('jenhen', 'password'),
('allsky', 'password'),
('olivad', 'password'),
('katjen', 'password'),
('sarkle', 'password'),
('niccla', 'password'),
('katdur', 'password'),
('amishe', 'password'),
('benler', 'password');

insert into `teacher` (`name`, `login`, `department`) values
('Kathleen Durant', 'katdur', 'College of Computer Science'),
('Amit Shesh', 'amishe', 'College of Computer Science'),
('Ben Lerner', 'benler', 'College of Computer Science');

insert into `tutor` (`name`, `login`) values
('Ben Clauss', 'bencla'),
('Joe Smith', 'joesmi'),
('Jim Johnson', 'jimjoh'),
('Jon Stewart', 'jonste'),
('Jen Henson', 'jenhen'),
('Allie Skywalker', 'allsky'),
('Olivia Vader', 'olivad'),
('Kat Jenovic', 'katjen'),
('Sarah Kleber', 'sarkle'),
('Nick Clark', 'niccla');

insert into `course` (`name`, `term`, `year`, `location`, `teacher_id`, `weekday`, `start_time`, `end_time`) values
('Database Design', 'Fall', 2016, 'Robinson Hall', 3, 'Monday,Wednesday,Thursday', '16:35', '17:40'),
('Objected-Oriented Design', 'Fall', 2016, 'Hurtig Hall', 1, 'Tuesday,Friday', '13:35', '15:15'),
('Fundamentals of Computer Science I', 'Spring', 2016, 'West Village F', 2, 'Monday,Wednesday,Thursday', '13:35', '14:40'),
('Logic and Computation', 'Spring', 2016, 'Behrakis Hall', 3, 'Monday,Wednesday,Thursday', '10:30', '11:35'),
('Discrete Structures', 'Fall', 2015, 'Snell Library', 1, 'Monday,Wednesday,Thursday', '16:35', '17:40');

insert into `office_hours` (`location`, `weekday`, `start_time`, `end_time`, `tutor_id`, `course_id`) values
('WVH 362', 'Monday', '11:45', '12:45', 4, 5),
('WVH 421', 'Tuesday', '13:50', '14:50', 1, 1),
('WVH 122', 'Wednesday', '9:10', '10:10', 2, 2),
('WVH 117', 'Monday', '11:45', '12:45', 3, 3),
('WVH 334', 'Tuesday', '14:40', '16:10', 4, 4),
('WVH 460', 'Monday', '9:10', '10:40', 5, 3),
('WVH 402', 'Wednesday', '13:50', '15:20', 6, 2),
('WVH 312', 'Wednesday', '17:45', '18:45', 7, 2),
('WVH 332', 'Tuesday', '17:45', '19:15', 8, 1),
('WVH 110', 'Tuesday', '11:45', '12:45', 9, 4);
