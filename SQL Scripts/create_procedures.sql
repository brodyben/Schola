use schola;

drop procedure if exists add_tutor;
delimiter $$
create procedure add_tutor
(
  in name varchar(30),
  in username varchar(10),
  in password varchar(10)
) 
begin 
  insert into `user` (`username`, `password`)
  values (username, password);
  
  insert into `tutor` (`name`, `login`)
  values (name, username);
end$$
delimiter ;
 
drop procedure if exists delete_tutor;
delimiter $$
create procedure delete_tutor
(
  in tutor_id int
)
begin
  delete from `tutor` where `id` = tutor_id;
end$$
delimiter ;

drop procedure if exists add_office_hours;
delimiter $$
create procedure add_office_hours
(
  in location varchar(20),
  in weekday enum('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'),
  in start_time time,
  in end_time time,
  in tutor_id int,
  in course_id int
)
begin 
  insert into `office_hours` (`location`, `weekday`, `start_time`, `end_time`, `tutor_id`, `course_id`)
  values (location, weekday, start_time, end_time, tutor_id, course_id);
end$$
delimiter ;

drop procedure if exists update_office_hours;
delimiter $$
create procedure update_office_hours
(
  in office_hours_id int,
  in location varchar(20),
  in weekday enum('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'),
  in start_time time,
  in end_time time,
  in tutor_id int,
  in course_id int
) 
begin 
  update `office_hours` 
  set `location`=location, `weekday`=weekday, `start_time`=start_time, `end_time`=end_time, 
  `tutor_id`=tutor_id, `course_id`=course_id
  where `id`=office_hours_id;
end$$
delimiter ;
 
drop procedure if exists delete_office_hours;
delimiter $$
create procedure delete_office_hours
(
  in office_hours_id int
) 
begin 
  delete from `office_hours` WHERE `id`=office_hours_id;
end$$
delimiter ;
