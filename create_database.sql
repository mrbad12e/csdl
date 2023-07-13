drop database if exists shopcart;
create database shopcart;
\c shopcart

create table users(
    id char(8) primary key,
    email varchar(50) unique,
    passw varchar(50) not null,
    datejoined date default current_date,
    last_login date default current_date,
    is_active boolean default True,
    is_staff boolean default False,
    is_admin boolean default False,
    is_superadmin boolean default False
);

create table user_profile(
    id char(8) primary key,
    images varchar(50) default 'images/avatars/avatar2.jpg',
    first_name text null,
    last_name text null,
    first_address text null,
    second_address text null,
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
    label text not null,
    variation_value text null,
    created_date date default current_date,
    is_active boolean default True,
    constraint prod_id_fk_product foreign key (prod_id) references product(id)
);

create table cart(
    id varchar(20) primary key,
    user_id char(8),
    date_added date default current_date,
    is_valid boolean,
    total_price decimal default 0,
    constraint user_id_fk_user foreign key (user_id) references users(id)
);

create table cartitem(
    prod_id char(8) not null,
    cart_id varchar(20) not null, 
    variation_id char(12) null,
    quantity int default 1,
    sub_total decimal not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp,

    constraint prod_id_fk_product foreign key (prod_id) references product(id),
    constraint variation_id_fk_var foreign key (variation_id) references variation(id),
    constraint cart_id_fk_cart foreign key (cart_id) references cart(id)
);

create table payment(
    id varchar(20) primary key,
    user_id char(8) not null,
    cart_id varchar(20) not null,
    status varchar(10) default 'delay' check (status in ('success', 'denied', 'delay')),
    amount_paid decimal not null,

    first_name text,
    last_name text,
    phone text,
    email text,
    first_address text,
    second_address text,
    country text,
    state text,
    city text,

    payment_method varchar default 'online',
    created_at timestamp default current_timestamp,

    constraint user_id_fk_user foreign key (user_id) references users(id),
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
    order_id varchar(20) not null,
    prod_id char(8) not null,
    variation_id char(12) null,

    quantity int,
    prod_price decimal,
    ordered boolean default True,
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