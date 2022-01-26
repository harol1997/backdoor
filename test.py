from browser_history.browsers import Edge
f = Edge()
outputs = f.fetch_history()
his = outputs.save("hola", "csv")
print(his)