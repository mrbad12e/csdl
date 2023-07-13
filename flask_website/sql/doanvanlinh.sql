--cau 1:

--them san pham vao cartitem co so luong
CREATE OR REPLACE FUNCTION add_to_cart(prod_id CHAR(8), variation_id CHAR(12), user_id CHAR(8))
RETURNS VOID AS $$
DECLARE
    cartid CHAR(20);
    total DECIMAL;
BEGIN
    IF EXISTS (
        SELECT 1
        FROM cart
        WHERE cart.user_id = $3
            AND cart.is_valid = true
    ) THEN -- User has a valid cart
        SELECT INTO cartid id FROM cart
        WHERE cart.user_id = $3 AND cart.is_valid = true;
        
        SELECT price INTO total FROM product WHERE id = $1;

        IF EXISTS (
            SELECT 1
            FROM cartitem
            WHERE cartitem.prod_id = $1
                AND cartitem.cart_id = cartid
                and cartitem.variation_id = $2
        ) THEN -- Product already exists in the cart
            RAISE NOTICE 'Update so luong';
            UPDATE cartitem
            SET quantity = quantity + 1,
                updated_at = current_timestamp,
            WHERE cartitem.prod_id = $1
                AND cartitem.cart_id = cartid;
                and cartitem.variation_id = $2
        ELSE -- New product to be added to the cart
            RAISE NOTICE 'Them moi';
            INSERT INTO cartitem (prod_id, cart_id, variation_id, quantity, sub_total)
            VALUES ($1, cartid, $2, 1, total);
        END IF;
    ELSE -- User doesn't have a valid cart
        RAISE NOTICE 'Tao gio hang va them moi';
        SELECT SUBSTRING('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' FROM (random() * 52 + 1)::integer FOR 20)
        INTO cartid;
        INSERT INTO cart (id, user_id, is_valid)
        VALUES (cartid, $3, true);
        INSERT INTO cartitem (prod_id, cart_id, variation_id, quantity, sub_total)
        VALUES ($1, cartid, $2, 1, 0);
    END IF;
END;
$$ LANGUAGE plpgsql;



--cau 2:
--check khi them vao cart quantity ko qua stock
create or replace function check_quantity_tf() 
returns trigger as $$
begin
 IF TG_OP = 'INSERT' THEN
        IF NEW.quantity > (
            SELECT stock FROM product WHERE id = NEW.prod_id
        ) THEN
            RAISE EXCEPTION 'Số lượng vượt quá số lượng trong kho.';
			else
return new;
	   end if;
	   end if;
 if  TG_OP = 'UPDATE' then 
IF NEW.quantity+OLD.quantity > (
            SELECT stock FROM product WHERE id = NEW.prod_id
        ) THEN
            RAISE EXCEPTION 'Số lượng vượt quá số lượng trong kho.';
			else
	 return new;
end if;
end if;
end;
$$ language plpgsql;

CREATE or replace TRIGGER check_quantity
BEFORE UPDATE or insert ON cartitem
FOR EACH ROW
EXECUTE PROCEDURE check_quantity_tf();
--cau 3:
--xoa khoi cartitem khi quantity ve 0
CREATE OR REPLACE FUNCTION delete_product_when_quantity_zero()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.quantity = 0 THEN
        delete FROM cartitem WHERE cartitem.cart_id = NEW.cart_id and cartitem.prod_id=NEW.prod_id;
		return null;
    else
    RETURN NEW;
	end if;
END;
$$ LANGUAGE plpgsql;

CREATE or replace TRIGGER delete_orderproduct_trigger_tf
AFTER UPDATE ON cartitem
FOR EACH ROW
EXECUTE PROCEDURE delete_product_when_quantity_zero();

--cau 4
--func delete so luong
create or replace function delete_from_cartitem(cart_id char(8), variation_id char(12), quantity integer)
returns void as $$
begin
    update cartitem set quantity =cartitem.quantity-$3 where cartitem.variation_id=$2 and cartitem.cart_id=cart_id;
end;
$$language plpgsql;

--cau 5:
-- tu dong cap nhat sub_total trong cartitem
CREATE OR REPLACE FUNCTION update_sub_total_tf()
RETURNS TRIGGER AS $$
declare prod_price decimal;
BEGIN
select into prod_price price from product where product.id=new.prod_id;
new.sub_total:=new.quantity * prod_price;
return new;
END;
$$ LANGUAGE plpgsql;

CREATE or replace TRIGGER update_sub_total_trigger
BEFORE UPDATE or INSERT ON cartitem
FOR EACH ROW
EXECUTE PROCEDURE update_sub_total_tf();

--cau 6:
-- tu dong cap nhat total_price cua cart
create or replace function update_total_price_tf()
returns trigger as $$
declare total decimal;
declare id_user char(8);
begin
	select into id_user user_id from cart where cart.id= new.cart_id;
    select into total sum(sub_total) from cartitem where cartitem.cart_id=new.cart_id;
    update cart set total_price = total where cart.user_id=id_user and is_valid =True;
    return new;
end;
$$ language plpgsql;

create or replace trigger update_total_price_trigger
AFTER UPDATE or INSERT ON cartitem
for each ROW
execute PROCEDURE update_total_price_tf();