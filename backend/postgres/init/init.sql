GRANT ALL PRIVILEGES ON DATABASE time_tracker_db TO tracker;

create table projects(
    id serial NOT NULL,
    name text NOT NULL,
    description TEXT,
    primary key(id)
);

create table time_entries(
    id serial NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    project_id integer,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    primary key(id)
);


INSERT into projects(
    id, name, description
) values
(1, 'work', 'working hard'),
(2, 'study', NULL),
(3, 'training', 'lifting weights');


INSERT into time_entries(
    id, start_time, end_time, project_id
) values
(1, '2024-01-13 12:30', '2024-01-13 15:45', 1),
(3, '2024-01-13 13:30', '2024-01-13 15:45', 1),
(2, '2024-01-20 22:30', NULL, NULL);
