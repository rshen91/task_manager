INSERT INTO users (username, first_name, last_name, password, profile_img, email, time_zone)
VALUES ('Minnie', 'Minnie', 'Mouse', 'MouseGal', 'static/img/minnie.jpg', 'minnie@mouse.purr', 'PST'),
('LadyFlash', 'Lady', 'Flash', 'PowerfulLady', 'static/img/ladyflash.jpg', 'lady@flash.pow', 'PST');

INSERT INTO tasks (task_name, due_date, priority, open_close_status, user_id, task_frequency, taskcat_name)
VALUES ('Do laundry', '10/31/16', 5, 0, 1, 'weekly', 'personal'),
('Meet with Ben', '11/15/16', 5, 0, 1, 'weekly', 'professional'),
('Meet with Ben', '11/22/16', 5, 0, 1, 'weekly', 'professional'),
('Meet with Ben', '11/29/16', 5, 0, 1, 'weekly', 'professional'),
('Meet with Ben', '12/06/16', 5, 0, 1, 'weekly', 'professional'),
('Buy ice cream', '10/01/16', 5, 1, 1, 'once', 'personal');

INSERT INTO goals (user_id, description, active_goal, time_toachieve, goalcat_name)
VALUES (1, 'Be a better communicator', 'True', 'month', 'professional');