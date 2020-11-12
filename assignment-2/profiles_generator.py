import censusname as censusname
import multiprocessing as mp


censusname.generate(nameformat='{surname}, {given}')

insert_statment = '''INSERT INTO profiles( 
                        first_name,
                        surname,
                        gender,
                        city,
                        user_id)
                        VALUES\n
                        '''
# with open('profiles_insert.sql', 'w') as profiles_script:
#     profiles_script.write(insert_statment)
#     for _ in range(1000000):
#         surname, name = censusname.generate(nameformat='{surname},{given}').split(',')
#         insert_record = f"('{name}','{surname}', 0, 'Moscow',1),\n"
#         profiles_script.write(insert_record)

def generate_profiles(r):
    cens = censusname.Censusname()
    insert_record = ''
    for _ in range(r):
        surname, name = cens.generate(nameformat='{surname},{given}').split(',')
        insert_record += f"('{name}','{surname}', 0, 'Moscow',1),\n"
    return insert_record

if __name__ == '__main__':    
    pool = mp.Pool(processes = 4)
    for i in range(19, 25):
        totals = pool.map(generate_profiles, (10000, 10000, 10000, 10000))
        with open(f'./db/assignment-2/profiles_insert{i}.sql', 'w') as profiles_script:
            profiles_script.write(insert_statment)
            for t in totals:
                profiles_script.write(t)
