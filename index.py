import firebirdsql
conn = firebirdsql.connect(
    host='localhost',
    database='C:\\Users\Maiconkkl\\Desktop\\DATAGES.fdb',
    port=3050,
    user='SYSDBA',
    password='masterkey'
)
notas = conn.cursor()
notas.execute("SELECT VENDAS.NOTA FROM VENDAS WHERE VENDAS.PROCESSADA = 0 AND VENDAS.MODELO = 'D' AND VENDAS.VALOR_TOT_PRO > 0")
for nota in notas.fetchall():
    prods = conn.cursor()
    prods.execute("SELECT ITEVENDAS.CODIGO FROM ITEVENDAS WHERE ITEVENDAS.NOTA = '" + nota[0]+ "'")
    for prod in prods.fetchall():
        prod_update = conn.cursor()
        prod_update.execute("UPDATE ESTOQUE SET ESTOQUE.QTD = ESTOQUE.QTD - 1 WHERE ESTOQUE.CODIGO = '" + prod[0] + "'")
        prod_update.fetchone()
    nota_update = conn.cursor()
    nota_update.execute("UPDATE VENDAS SET VENDAS.PROCESSADA = 1 WHERE VENDAS.PROCESSADA = 0 AND "
                        "VENDAS.MODELO = 'D' "
                        "AND VENDAS.VALOR_TOT_PRO > 0 "
                        "AND VENDAS.NOTA = '" + nota[0]+ "'")
    nota_update.fetchone()

conn.commit()
conn.close()