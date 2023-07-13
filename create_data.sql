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

insert into variation (id, prod_id, label, variation_value) values ('000000000001', '00000001', 'color', 'red');
insert into variation (id, prod_id, label, variation_value) values ('000000000002', '00000001', 'color', 'green');
insert into variation (id, prod_id, label, variation_value) values ('000000000003', '00000001', 'color', 'blue');
insert into variation (id, prod_id, label, variation_value) values ('000000000004', '00000001', 'color', 'white');
insert into variation (id, prod_id, label, variation_value) values ('000000000005', '00000002', 'color', 'red');
insert into variation (id, prod_id, label, variation_value) values ('000000000006', '00000002', 'color', 'green');
insert into variation (id, prod_id, label, variation_value) values ('000000000007', '00000002', 'color', 'blue');
insert into variation (id, prod_id, label, variation_value) values ('000000000008', '00000002', 'color', 'white');
insert into variation (id, prod_id, label, variation_value) values ('000000000009', '00000003', 'color', 'red');
insert into variation (id, prod_id, label, variation_value) values ('000000000010', '00000003', 'color', 'green');
insert into variation (id, prod_id, label, variation_value) values ('000000000011', '00000003', 'color', 'blue');
insert into variation (id, prod_id, label, variation_value) values ('000000000012', '00000003', 'color', 'white');
insert into variation (id, prod_id, label, variation_value) values ('000000000013', '00000004', 'color', 'red');
insert into variation (id, prod_id, label, variation_value) values ('000000000014', '00000004', 'color', 'green');
insert into variation (id, prod_id, label, variation_value) values ('000000000015', '00000004', 'color', 'blue');
insert into variation (id, prod_id, label, variation_value) values ('000000000016', '00000004', 'color', 'white');
insert into variation (id, prod_id, label, variation_value) values ('000000000017', '00000005', 'color', 'red');
insert into variation (id, prod_id, label, variation_value) values ('000000000018', '00000005', 'color', 'green');
insert into variation (id, prod_id, label, variation_value) values ('000000000019', '00000005', 'color', 'blue');
insert into variation (id, prod_id, label, variation_value) values ('000000000020', '00000005', 'color', 'white');
insert into variation (id, prod_id, label, variation_value) values ('000000000021', '00000006', 'color', 'red');
insert into variation (id, prod_id, label, variation_value) values ('000000000022', '00000006', 'color', 'green');
insert into variation (id, prod_id, label, variation_value) values ('000000000023', '00000006', 'color', 'blue');
insert into variation (id, prod_id, label, variation_value) values ('000000000024', '00000006', 'color', 'white');
insert into variation (id, prod_id, label, variation_value) values ('000000000025', '00000007', 'color', 'red');
insert into variation (id, prod_id, label, variation_value) values ('000000000026', '00000007', 'color', 'green');
insert into variation (id, prod_id, label, variation_value) values ('000000000027', '00000007', 'color', 'blue');
insert into variation (id, prod_id, label, variation_value) values ('000000000028', '00000007', 'color', 'white');
insert into variation (id, prod_id, label, variation_value) values ('000000000029', '00000008', 'color', 'red');
insert into variation (id, prod_id, label, variation_value) values ('000000000030', '00000008', 'color', 'green');
insert into variation (id, prod_id, label, variation_value) values ('000000000031', '00000008', 'color', 'blue');
insert into variation (id, prod_id, label, variation_value) values ('000000000032', '00000008', 'color', 'white');
insert into variation (id, prod_id, label, variation_value) values ('000000000033', '00000009', 'color', 'red');
insert into variation (id, prod_id, label, variation_value) values ('000000000034', '00000009', 'color', 'green');
insert into variation (id, prod_id, label, variation_value) values ('000000000035', '00000009', 'color', 'blue');
insert into variation (id, prod_id, label, variation_value) values ('000000000036', '00000009', 'color', 'white');
insert into variation (id, prod_id, label, variation_value) values ('000000000037', '00000010', 'color', 'red');
insert into variation (id, prod_id, label, variation_value) values ('000000000038', '00000010', 'color', 'green');
insert into variation (id, prod_id, label, variation_value) values ('000000000039', '00000010', 'color', 'blue');
insert into variation (id, prod_id, label, variation_value) values ('000000000040', '00000010', 'color', 'white');
insert into variation (id, prod_id, label, variation_value) values ('000000000041', '00000011', 'color', 'red');
insert into variation (id, prod_id, label, variation_value) values ('000000000042', '00000011', 'color', 'green');
insert into variation (id, prod_id, label, variation_value) values ('000000000043', '00000011', 'color', 'blue');
insert into variation (id, prod_id, label, variation_value) values ('000000000044', '00000011', 'color', 'white');
insert into variation (id, prod_id, label, variation_value) values ('000000000045', '00000012', 'color', 'red');
insert into variation (id, prod_id, label, variation_value) values ('000000000046', '00000012', 'color', 'green');
insert into variation (id, prod_id, label, variation_value) values ('000000000047', '00000012', 'color', 'blue');
insert into variation (id, prod_id, label, variation_value) values ('000000000048', '00000012', 'color', 'white');