drop table if exists logs;
drop table if exists cars;

create table cars(
	car_id varchar(50) primary key,
	name varchar(100),
	room_no varchar(20),
	contact_number varchar(20)
);

create table logs(
	log_id serial,
	curr_date varchar(50),
	curr_time varchar(50),
	car_id varchar(50),
	constraint car_id
	foreign key (car_id)
	references cars(car_id)
);

insert into cars values('KA 05 NB 1786' , 'Dr Abul Hamid Shaikh', 'B 101','8907651234');
insert into logs(curr_date,curr_time,car_id) values(current_date,current_time::time,'KA 05 NB 1786')