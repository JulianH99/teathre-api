create table document_type (
    document_type_id number generated as identity ,
    name varchar(50) not null,
    constraint DCTPPK primary key (document_type_id)
);


CREATE table person (
    doc_number varchar(11),
    document_type_id number not null,
    names varchar(50),
    last_name varchar(50),
    birth_date Date,
    email varchar(100),
    constraint PERPK primary key(doc_number),
    constraint DCTPFK foreign key (document_type_id) references document_type(document_type_id)
);

create table career(
    career_id number generated as identity,
    name varchar(150) not null,
    constraint CRPK primary key (career_id)
);


create table student (
    doc_number varchar(11),
    code varchar(12),
    career_id number not null,
    constraint STPK primary key (doc_number, code),
    constraint CRFK foreign key (career_id) references career(career_id),
    constraint PERFK foreign key (doc_number) references person(doc_number)
);

create table play_type(
    play_type_id number generated as identity ,
    name varchar(20) not null,
    constraint PLTYPK primary key (play_type_id)
);

create table country (
    code varchar(4),
    name varchar(30),
    constraint CNTRPK primary key  (code)
);

create table play(
    play_id number generated as identity ,
    play_type_id number not null,
    title varchar(250),
    writer varchar(200),
    writing_year integer,
    country_code varchar(4) not null,
    constraint PLPK primary key (play_id),
    constraint PLTYFK foreign key (play_type_id) references play_type(play_type_id),
    constraint CNTRFK  foreign key (country_code) references country(code)
);


create table convocation(
    id number generated as identity ,
    play_id number not null,
    start_date date not null,
    end_date date not null,
    constraint CNVPK primary key (id),
    constraint PLFK foreign key (play_id) references play(play_id)
);

create table convocation_applicant(
    convocation_id number generated as identity ,
    student_code varchar(12) not null,
    doc_number varchar(11),
    constraint CNVNPLNTPK primary key (convocation_id, student_code, doc_number),
    constraint STFK foreign key (student_code, doc_number) references student(code, doc_number),
    constraint CNVFK foreign key (convocation_id) references convocation(id)
);

