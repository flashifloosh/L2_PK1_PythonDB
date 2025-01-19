from Database import Database


class CertificateUtil:

    @classmethod
    def get_cert(cls, student):
        Database.connect()
        query = 'SELECT subject, grade FROM certificate WHERE student = ?'
        Database.cursor.execute(query, (student,))
        certificate = Database.cursor.fetchall()
        Database.close()
        return certificate
