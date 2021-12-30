name = input("Nombre del titular: ")
interest_rate = float(input("Tasa de interés: "))
loan = float(input("Deuda actual: $"))

invalid = True
while invalid:
    payment = float(input("Pago a realizar: $"))
    if payment > loan:
        print("No es posible realizar un pago mayor a la deuda actual. Intrpduce una nueva cantidad")
    else:
        invalid = False

new_charges = float(input("Nuevos cargos: $"))

monthly_interest = interest_rate / 12
recalculated_loan = (loan - payment) * (1 + monthly_interest)
new_loan = recalculated_loan + new_charges

print("\n- - - DATOS DE LA TARJETA SOLICITADA - - -\n")
print(f"Nombre del titular: {name}")
print(f"Tasa de interés: {interest_rate}%")
print(f"Deuda actual: ${loan}")
print(f"Pago realizado: ${payment}")
print(f"Cargos nuevos: ${new_charges}")
new_loan = "${:,.2f}".format(new_loan)


print("\nDEUDA ACTUALIZADA")
print(f"Próximo pago mensual: {new_loan}")
