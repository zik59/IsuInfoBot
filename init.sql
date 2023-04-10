CREATE TABLE students(
                    id SERIAL PRIMARY KEY,
                    isu_id text,
                    variant varchar(2),
                    isu_group varchar(10),
                    image text,
                    name varchar(70)
                );