from database.DB_connect import DBConnect
from model.Constructor import Constructor
from model.arco import Arco


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getNodi(anno1, anno2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
from constructors c 
where c.constructorId in (select constructorId
from results r1, races r
where r.raceid = r1.raceid and 
r1.position is not null and r.year between %s and %s)"""
        cursor.execute(query, [anno1, anno2])

        for row in cursor:
            costruttore = Constructor(**row)
            results.append(costruttore)

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getArchi(anno1, anno2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """with piloti as (select constructorId, driverId 
from results r1, races r
where r.raceid = r1.raceid and 
r1.position is not null and r.year between %s and %s
group by constructorId, driverId) 

select p1.constructorId as nodo1, p2.constructorId as nodo2, count(distinct p1.driverId) as peso
from piloti p1, piloti p2
where p1.driverId = p2.driverId and p1.constructorId>p2.constructorId
group by p1.constructorId, p2.constructorId"""
        cursor.execute(query,[anno1, anno2])

        for row in cursor:
            costruttore = Arco(**row)
            results.append(costruttore)

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAnni():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor()
        query = """select constructorId, max(dob)
from results r1, drivers d
where r1.driverId = d.driverId
group by constructorId"""
        cursor.execute(query)

        for row in cursor:
            results.append(row)

        cursor.close()
        conn.close()
        return results
