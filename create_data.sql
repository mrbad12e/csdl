\c shopcart
insert into users (id, email, passw, is_active)
values ('00000001', 'guest@example.com', 'guest', True);
insert into users (id, email, passw, is_active, is_admin, is_staff)
values ('00000002', 'admin@example.com', 'guest', True, True, True);

insert into category (name) values ('T-shirt');
insert into category (name) values ('Shirt');
insert into category (name) values ('Shoes');
insert into category (name) values ('Pants');
insert into category (name) values ('Jacket');
insert into category (name) values ('Short Pants');
insert into category (name) values ('Package');
insert into category (name) values ('Jeans');

insert into product (id, slug, description, price, category_name, stock) 
values ('00000001', 'images/items/1.jpg', 'Brad T-shirt', 10, 'T-shirt', 100);
insert into product (id, slug, description, price, category_name, stock) 
values ('00000002', 'images/items/2.jpg', 'Polo Jacket', 10, 'Jacket', 100);
insert into product (id, slug, description, price, category_name, stock) 
values ('00000003', 'images/items/3.jpg', 'Short Pant', 10, 'Short Pants',100);
insert into product (id, slug, description, price, category_name, stock) 
values ('00000004', 'images/items/4.jpg', 'Kanken Package', 10, 'Package', 100);
insert into product (id, slug, description, price, category_name, stock) 
values ('00000005', 'images/items/12.jpg', 'Adiddas Shoes', 10, 'Shoes', 100);
insert into product (id, slug, description, price, category_name, stock) 
values ('00000006', 'images/items/ATX-Jeans.jpg', 'ATX-Jeans', 10, 'Jeans', 100);
insert into product (id, slug, description, price, category_name, stock) 
values ('00000007', 'images/items/Blue-Shirt.jpg', 'Blue-Shirt', 10, 'Shirt', 100);
insert into product (id, slug, description, price, category_name, stock) 
values ('00000008', 'images/items/Great-Tshirt.jpg', 'Great-Tshirt', 10, 'T-shirt', 100);
insert into product (id, slug, description, price, category_name, stock) 
values ('00000009', 'images/items/jordan-true-flight-basketball-shoes.jpg', 'Basketball Shoes', 10, 'Shoes', 100);
insert into product (id, slug, description, price, category_name, stock) 
values ('00000010', 'images/items/Puma-Ferrari-Shoes.jpg', 'Puma Ferrari Shoes', 10, 'Shoes', 100);
insert into product (id, slug, description, price, category_name, stock) 
values ('00000011', 'images/items/Mavi_jeans.jpg', 'Mavi Jeans', 10, 'Jeans', 100);
insert into product (id, slug, description, price, category_name, stock) 
values ('00000012', 'images/items/Wrangler-Shirt.jpg', 'Wrangler Shirt', 10, 'Shirt', 100);
