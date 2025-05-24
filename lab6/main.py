from hash_table import HashTable
table=HashTable(5)
table.insert("Математика", "Лже-наука")
print(table.search("Математика"))
table.update("Математика", "Не лже-наука")
print(table.search("Математика"))
table.delete("Математика")
print(table.search("Математика"))