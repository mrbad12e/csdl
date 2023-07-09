drop database if exists shopcart;
create database shopcart;
\c shopcart

create table users(
    id char(8) primary key,
    email varchar(50) unique,
    passw varchar(50) not null,
    first_name text,
    last_name text,
    datejoined date default current_date,
    last_login date default current_date,
    is_active boolean default True,
    is_staff boolean default False,
    is_admin boolean default False,
    is_superadmin boolean default False
);

create table user_profile(
    id char(8) primary key,
    first_address text,
    second_address text,
    city varchar(20),
    country varchar(20),
    constraint profile_fk_user foreign key (id) references users(id)
);

create table category(
    name varchar(30) primary key,
    slug varchar(255),
    description text
);

create table product(
    id char(8) primary key,
    slug varchar(255),
    description text,
    price decimal not null,
    category_name varchar(30) not null,
    created_date date default current_date,
    modified_date date default current_date,
    stock int default 0,
    constraint category_name_fk_category foreign key (category_name) references category(name)
);

create table variation(
    id char(12) primary key,
    prod_id char(8) not null,
    variation_value text null,
    created_date date default current_date,
    is_active boolean,
    constraint prod_id_fk_product foreign key (prod_id) references product(id)
);

create table cart(
    id varchar(20) primary key,
    user_id char(8) not null,
    date_added date default current_date,
    constraint user_id_fk_user foreign key (user_id) references users(id)
);

create table cartitem(
    id varchar(30) primary key,
    prod_id char(8) not null,
    cart_id varchar(20) not null, 
    variation_id char(12) null,
    quantity int default 1,

    constraint prod_id_fk_product foreign key (prod_id) references product(id),
    constraint variation_id_fk_var foreign key (variation_id) references variation(id),
    constraint cart_id_fk_cart foreign key (cart_id) references cart(id)
);

create table voucher(
    id varchar(20) primary key,
    user_id char(8) not null,
    percentage decimal(2),
    limit_discount decimal,
    valid_from date default current_date,
    expiry_date date default '2023-08-01',
    label text not null,
    constraint user_id_fk_user foreign key (user_id) references users(id)
);

create table payment(
    id varchar(20) primary key,
    user_id char(8) not null,
    voucher_id varchar(20) null,
    cart_id varchar(20) not null,

    payment_method varchar default 'online',
    amount_paid decimal not null,
    status varchar(10) default 'success' check (status in ('success', 'denied', 'delay')),
    created_at timestamp default current_timestamp,
    
    constraint user_id_fk_user foreign key (user_id) references users(id),
    constraint voucher_id_fk_voucher foreign key (voucher_id) references voucher(id),
    constraint cart_id_fk_cart foreign key (cart_id) references cart(id)
);

create table orders(
    id varchar(20) primary key,
    user_id char(8) not null,
    payment_id varchar(20) not null,

    status varchar(10) default 'new' check (status in ('new', 'old', 'wait')),
    is_ordered boolean default TRUE,
    total_price decimal,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp,

    constraint user_id_fk_user foreign key (user_id) references users(id),
    constraint payment_id_fk_payment foreign key (payment_id) references payment(id)
);

create table orderproduct(
    id varchar(20) primary key,
    order_id varchar(20) not null,
    prod_id char(8) not null,
    variation_id char(12) null,

    quantity int,
    prod_price decimal,
    ordered boolean default False,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp,

    constraint prod_id_fk_product foreign key (prod_id) references product(id),
    constraint variation_id_fk_var foreign key (variation_id) references variation(id),
    constraint order_id_fk_order foreign key (order_id) references orders(id)
);

create table ReviewRating (
    id varchar(20) primary key,
    user_id char(8) not null,
    prod_id char(8) not null,

    subject text default null,
    review text default null,
    rate decimal(2),
    status boolean default True,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp,

    constraint prod_id_fk_product foreign key (prod_id) references product(id),
    constraint user_id_fk_user foreign key (user_id) references users(id)
);