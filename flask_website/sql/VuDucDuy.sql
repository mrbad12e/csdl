--tao profile khi nhet dc 1 users id vo 
CREATE OR REPLACE FUNCTION tf_create_profile()
RETURNS TRIGGER AS $$
BEGIN
	insert into user_profile(id) values(new.id);
	return new;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER tg_create_profile
AFTER INSERT ON users
FOR EACH ROW 
EXECUTE PROCEDURE tf_create_profile();

--Check mail truoc khi them vao 
CREATE OR REPLACE FUNCTION tf_check_mail()
RETURNS TRIGGER AS $$
BEGIN
if exists(select 1 from users where users.email= new.email) then
	raise notice 'Email da ton tai';
	return null;
	else
	raise notice 'Tao tai khoan thanh cong';
	return new;
end if;
END;
$$ LANGUAGE plpgsql;

CREATE or replace TRIGGER tg__check_mail
BEFORE INSERT ON users
FOR EACH ROW 
EXECUTE PROCEDURE tf_check_mail();

--check dieu kien truoc khi review
CREATE OR REPLACE FUNCTION tf_check_review_condition()
RETURNS TRIGGER AS $$
BEGIN
if exists(select 1 from payment, orders, orderproduct  
			where payment.user_id =new.user_id 
			and prod_id = new.prod_id 
			and payment.id = orders.payment_id 
			and orders.id = orderproduct.order_id)
then 
    update product set avgrate = (select AVG(rate) from reviewrating where prod_id = new.prod_id) where id = new.prod_id;
    raise notice 'Review san pham thanh cong'; 
    return new;
else raise notice 'Ban chua mua hang';
return null;
end if;
END;
$$ LANGUAGE plpgsql;

CREATE or replace TRIGGER tg_check_review_condition
BEFORE INSERT ON reviewrating
FOR EACH ROW 
EXECUTE PROCEDURE tf_check_review_condition();

--trigger upd stock
CREATE OR REPLACE FUNCTION tf_update_stock()
RETURNS TRIGGER AS $$
BEGIN
UPDATE product set stock = stock - new.quantity where id = new.prod_id;
return new;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER tg_update_stock
AFTER INSERT ON orderproduct
FOR EACH ROW 
EXECUTE PROCEDURE tf_update_stock();