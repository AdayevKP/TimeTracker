GRANT ALL PRIVILEGES ON DATABASE time_tracker_db TO tracker;

create table projects(
    id serial,
    name text NOT NULL,
    description TEXT,
    primary key(id)
);

create table time_entries(
    id serial,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    project_id integer,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    primary key(id)
);


INSERT into projects(
    name, description
) values
('work', 'working hard'),
('study', NULL),
('training', 'lifting weights');


INSERT into time_entries(
    start_time, end_time, project_id
) values
('2024-01-13 12:30', '2024-01-13 15:45', 1),
('2024-01-20 22:30', NULL, NULL);
