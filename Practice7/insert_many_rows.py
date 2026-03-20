# import psycopg2
# from config import load_config

# def insert_many_vendors(vendor_list):
#     """INSERT multiple vendors into the vendors table"""

#     sql = "INSERT INTO vendors(vendor_name) VALUES(%s) RETURNING *"
#     config=load_config()
#     try:
#         with psycopg2.connect(**config) as conn:
#             with conn.cursur() as cur:
#                 cur.executemany(sql, vendor_list)

#             conn.commit()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)

# if __name__=='__main__':
#     insert_vendor("3M Co.")

#     insert_many_vendors([
#         ('AKM Semiconductor Inc.',),
#         ('Asahi Glass Co Ltd.',),
#         ('Daikin Industries Ltd.',)
#     ])