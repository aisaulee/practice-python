
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR, 
    p_phone VARCHAR, 
    p_type VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN

    SELECT id INTO v_contact_id FROM contacts WHERE first_name = p_contact_name;

    IF v_contact_id IS NOT NULL THEN
        INSERT INTO phones (contact_id, phone, type)
        VALUES (v_contact_id, p_phone, p_type);
        RAISE NOTICE 'Телефон добавлен контакту %', p_contact_name;
    ELSE
        RAISE NOTICE 'Контакт с именем % не найден', p_contact_name;
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR, 
    p_group_name VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_group_id INTEGER;
BEGIN

    INSERT INTO groups (name) 
    VALUES (p_group_name)
    ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
    RETURNING id INTO v_group_id;

    UPDATE contacts 
    SET group_id = v_group_id 
    WHERE first_name = p_contact_name;

    IF NOT FOUND THEN
        RAISE NOTICE 'Контакт % не найден', p_contact_name;
    ELSE
        RAISE NOTICE 'Контакт % перемещен в группу %', p_contact_name, p_group_name;
    END IF;
END;
$$;

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    contact_id INTEGER,
    contact_name VARCHAR,
    contact_email VARCHAR,
    group_name VARCHAR,
    phone_numbers TEXT
) 
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id, 
        c.first_name, 
        c.email, 
        g.name,
        string_agg(p.phone || ' (' || p.type || ')', ', ') 
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.first_name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
    GROUP BY c.id, g.name;
END;
$$;