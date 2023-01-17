INSERT INTO users (email, "password", "name", surname, created_by, created_date, updated_by, updated_date) VALUES('testuser@gmail.com', '689601a4bd4d60a594c6c8697639f27cd420b7f939be3ef4bc1d6e1426ca1655', 'Mahmut', 'Aktaş', NULL, NULL, NULL, NULL);

INSERT INTO event_types ("name", service_name, created_by, created_date, updated_by, updated_date) VALUES('register', 'user-profile', 1, '2022-10-24 20:58:59.166', 1, '2022-10-24 21:00:23.274');

INSERT INTO event_type_fields (event_type_id, field_name, field_type, created_by, created_date, updated_by, updated_date) VALUES(1, 'username', 'String', 1, '2022-10-24 23:01:07.634', 1, '2022-10-24 23:06:35.270');
INSERT INTO event_type_fields (event_type_id, field_name, field_type, created_by, created_date, updated_by, updated_date) VALUES(1, 'register_date', 'DateTime', 1, '2022-10-25 22:53:44.830', NULL, NULL);
