\c shopcart
insert into users (id, email, passw, is_active)
values ('00000001', 'guest@example.com', 'guest', True);
insert into users (id, email, passw, is_active, is_admin, is_staff)
values ('00000002', 'admin@example.com', 'guest', True, True, True);

insert into category (name) values ('T-shirt');
insert into category (name) values ('Shirt');
insert into category (name) values ('Shoes');
insert into category (name) values ('Pants');

insert into product (id, description, price, category_name) 
values ('00000001', 'Brad T-shirt', 10, 'T-shirt');
insert into product (id, description, price, category_name) 
values ('00000002', 'Tim T-shirt', 10, 'T-shirt');
insert into product (id, description, price, category_name) 
values ('00000003', 'Jack T-shirt', 10, 'T-shirt');