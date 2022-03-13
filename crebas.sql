/*==============================================================*/
/* DBMS name:      ORACLE Version 12c                           */
/* Created on:     12/03/2022 19:07:59                          */
/*==============================================================*/


/*==============================================================*/
/* Table: activity                                              */
/*==============================================================*/
create table activity (
   activity_id          integer         generated as identity      not null,
   name                 varchar2(50)          not null,
   wage_per_hour        float                 not null,
   term_id              integer               not null,
   constraint pk_activity primary key (activity_id)
);

/*==============================================================*/
/* Table: country                                               */
/*==============================================================*/
create table country (
   code                 varchar2(3)           not null,
   name                 varchar2(70),
   constraint pk_country primary key (code)
);

/*==============================================================*/
/* Table: employee                                              */
/*==============================================================*/
create table employee (
   employee_id          integer      generated as identity         not null,
   unit_id              integer               not null,
   names                varchar2(40)          not null,
   last_names           varchar2(40)          not null,
   id_number            varchar2(11)          not null,
   phone_number         varchar2(10)          not null,
   email                varchar2(100)         not null,
   constraint pk_employee primary key (employee_id, unit_id)
);

/*==============================================================*/
/* Table: expense                                               */
/*==============================================================*/
create table expense (
   expense_code         varchar2(5)           not null,
   term_id              integer               not null,
   constraint pk_expense primary key (expense_code, term_id)
);

/*==============================================================*/
/* Table: play                                                  */
/*==============================================================*/
create table play (
   play_id              integer       generated as identity        not null,
   play_type_id         integer               not null,
   title                char(250)             not null,
   play_date            date                  not null,
   country_code         varchar2(3)           not null,
   state                smallint,
   writer_id            integer               not null,
   constraint pk_play primary key (play_id)
);

/*==============================================================*/
/* Table: play_activity                                         */
/*==============================================================*/
create table play_activity (
   play_activity_id     integer     generated as identity          not null,
   participant_id       integer               not null,
   employee_id          integer               not null,
   unit_id              integer               not null,
   play_event_id        integer               not null,
   play_id              integer               not null,
   activity_id          integer               not null,
   worked_hours         integer               not null,
   constraint pk_play_activity primary key (play_activity_id)
);

/*==============================================================*/
/* Table: play_character                                        */
/*==============================================================*/
create table play_character (
   id                   integer     generated as identity          not null,
   play_id              integer               not null,
   name                 varchar2(100)         not null,
   constraint pk_play_character primary key (id, play_id)
);

/*==============================================================*/
/* Table: play_event                                            */
/*==============================================================*/
create table play_event (
   play_event_id        integer      generated as identity         not null,
   play_id              integer               not null,
   theatre_id           integer               not null,
   event_type           integer               not null,
   "date"               date                  not null,
   start_time           date                  not null,
   end_time             date                  not null,
   constraint pk_play_event primary key (play_event_id, play_id)
);

/*==============================================================*/
/* Table: play_event_type                                       */
/*==============================================================*/
create table play_event_type (
   play_event_type_id   integer      generated as identity         not null,
   name                 varchar2(50)          not null,
   constraint pk_play_event_type primary key (play_event_type_id)
);

/*==============================================================*/
/* Table: play_expense                                          */
/*==============================================================*/
create table play_expense (
   play_expense_id      integer      generated as identity         not null,
   play_id              integer               not null,
   expense_code         varchar2(5)           not null,
   expense_date         date,
   term_id              integer               not null,
   constraint pk_play_expense primary key (play_expense_id, expense_code, term_id)
);

/*==============================================================*/
/* Table: play_participant                                      */
/*==============================================================*/
create table play_participant (
   participant_id       integer     generated as identity          not null,
   employee_id          integer               not null,
   unit_id              integer               not null,
   rol_id               integer,
   start_date           date                  not null,
   end_date             date,
   constraint pk_play_participant primary key (participant_id, employee_id, unit_id)
);

/*==============================================================*/
/* Table: play_type                                             */
/*==============================================================*/
create table play_type (
   play_type_id         integer       generated as identity        not null,
   name                 char(20)              not null,
   constraint pk_play_type primary key (play_type_id)
);

/*==============================================================*/
/* Table: role                                                  */
/*==============================================================*/
create table role (
   rol_id               integer     generated as identity          not null,
   name                 char(20),
   constraint pk_role primary key (rol_id)
);

/*==============================================================*/
/* Table: student                                               */
/*==============================================================*/
create table student (
   code                 char(12)              not null,
   unit_id              integer               not null,
   names                varchar2(50)          not null,
   last_names           varchar2(50)          not null,
   signup_date          date                  not null,
   birth_date           date                  not null,
   email                varchar2(100)         not null,
   constraint pk_student primary key (code)
);

/*==============================================================*/
/* Table: student_asistance                                     */
/*==============================================================*/
create table student_asistance (
   student_asistance_id integer       generated as identity        not null,
   play_event_id        integer               not null,
   play_id              integer               not null,
   student_code         char(12)              not null,
   constraint pk_student_asistance primary key (student_asistance_id)
);

/*==============================================================*/
/* Table: student_character                                     */
/*==============================================================*/
create table student_character (
   student_code         char(12)              not null,
   character_id         integer               not null,
   play_id              integer               not null,
   start_date           date                  not null,
   end_date             date,
   constraint pk_student_character primary key (student_code, character_id, play_id)
);

/*==============================================================*/
/* Table: term                                                  */
/*==============================================================*/
create table term (
   term_id              integer               not null,
   constraint pk_term primary key (term_id)
);

/*==============================================================*/
/* Table: theatre                                               */
/*==============================================================*/
create table theatre (
   id                   integer     generated as identity          not null,
   name                 varchar2(150)         not null,
   constraint pk_theatre primary key (id)
);

/*==============================================================*/
/* Table: unit                                                  */
/*==============================================================*/
create table unit (
   unit_id              integer      generated as identity         not null,
   unit_type_id         integer               not null,
   name                 varchar2(40)          not null,
   parent_unit_id       integer,
   constraint pk_unit primary key (unit_id)
);

/*==============================================================*/
/* Table: unit_type                                             */
/*==============================================================*/
create table unit_type (
   unit_type_id         integer       generated as identity        not null,
   name                 varchar2(30)          not null,
   description          varchar2(30)          not null,
   constraint pk_unit_type primary key (unit_type_id)
);

/*==============================================================*/
/* Table: writer                                                */
/*==============================================================*/
create table writer (
   writer_id            integer        generated as identity       not null,
   full_name            varchar2(50),
   country_code         varchar2(3)           not null,
   constraint pk_writer primary key (writer_id)
);

alter table activity
   add constraint fk_activity_belongs_t_term foreign key (term_id)
      references term (term_id);

alter table employee
   add constraint fk_employee_belongs_t_unit foreign key (unit_id)
      references unit (unit_id);

alter table expense
   add constraint fk_expense_has_many_term foreign key (term_id)
      references term (term_id);

alter table play
   add constraint fk_play_is_of_typ_play_typ foreign key (play_type_id)
      references play_type (play_type_id);

alter table play
   add constraint fk_play_was_playe_country foreign key (country_code)
      references country (code);

alter table play_activity
   add constraint fk_play_act_can_parti_play_par foreign key (participant_id, employee_id, unit_id)
      references play_participant (participant_id, employee_id, unit_id);

alter table play_activity
   add constraint fk_play_act_does_play_eve foreign key (play_event_id, play_id)
      references play_event (play_event_id, play_id);

alter table play_activity
   add constraint fk_play_act_gets_done_activity foreign key (activity_id)
      references activity (activity_id);

alter table play_character
   add constraint fk_play_cha_has_chara_play foreign key (play_id)
      references play (play_id);

alter table play_event
   add constraint fk_play_eve_consist_o_play foreign key (play_id)
      references play (play_id);

alter table play_event
   add constraint fk_play_eve_is_of_typ_play_eve foreign key (event_type)
      references play_event_type (play_event_type_id);

alter table play_event
   add constraint fk_play_eve_is_played_theatre foreign key (theatre_id)
      references theatre (id);

alter table play_expense
   add constraint fk_play_exp_has_play foreign key (play_id)
      references play (play_id);

alter table play_expense
   add constraint fk_play_exp_is_presen_expense foreign key (expense_code,term_id)
      references expense (expense_code, term_id);

alter table play_participant
   add constraint fk_play_par_has_role_role foreign key (rol_id)
      references role (rol_id);

alter table play_participant
   add constraint fk_play_par_relations_employee foreign key (employee_id, unit_id)
      references employee (employee_id, unit_id);

alter table student
   add constraint fk_student_belongs_t_unit foreign key (unit_id)
      references unit (unit_id);

alter table student_asistance
   add constraint fk_student__asists_in_student foreign key (student_code)
      references student (code);

alter table student_asistance
   add constraint fk_student__is_assist_play_eve foreign key (play_event_id, play_id)
      references play_event (play_event_id, play_id);

alter table student_character
   add constraint fk_student__is_played_play_cha foreign key (character_id, play_id)
      references play_character (id, play_id);

alter table student_character
   add constraint fk_student__plays_as_student foreign key (student_code)
      references student (code);

alter table unit
   add constraint fk_unit_belongs_t_unit foreign key (parent_unit_id)
      references unit (unit_id);

alter table unit
   add constraint fk_unit_is_of_typ_unit_typ foreign key (unit_type_id)
      references unit_type (unit_type_id);

alter table writer
   add constraint fk_writer_was_borne_country foreign key (country_code)
      references country (code);

