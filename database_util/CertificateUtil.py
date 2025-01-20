from Database import Database


class CertificateUtil:

    # Zusammenstellung des Zertifikats aus Note und Fachname. gibt dann für einen Schüler eine Liste aus, die aus allen Noten besteht.
    @classmethod
    def get_cert(cls, student):
        Database.connect()
        query = 'SELECT subject, grade FROM certificate WHERE student = ?'
        Database.cursor.execute(query, (student,))
        certificate = Database.cursor.fetchall()
        Database.close()
        return certificate
