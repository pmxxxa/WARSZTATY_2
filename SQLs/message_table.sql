CREATE TABLE Messages (
  id SERIAL PRIMARY KEY,
  from_id int,
  to_id int,
  text varchar,
  creation_date date,
  FOREIGN KEY (from_id) REFERENCES Users(id) ON DELETE CASCADE,
  FOREIGN KEY (to_id) REFERENCES Users(id) ON DELETE CASCADE
);