import streamlit as st
import io

def read_sales_file(file):
    lines = file.read().decode("utf-8").splitlines()
    data = []
    for line in lines:
        date, sale = line.split(",")
        data.append({"Fecha": date.strip(), "Venta": float(sale.strip())})
    return data

def calculate_statistics(data):
    total_sales = sum(entry["Venta"] for entry in data)
    average_sales = total_sales / len(data)
    max_sale_day = max(data, key=lambda x: x["Venta"])
    min_sale_day = min(data, key=lambda x: x["Venta"])
    return total_sales, average_sales, max_sale_day, min_sale_day

def save_statistics(total_sales, average_sales, max_sale_day, min_sale_day):
    output = io.StringIO()
    output.write(f"Venta total: {total_sales}\n")
    output.write(f"Promedio de ventas: {average_sales}\n")
    output.write(f"Día de mayor venta: {max_sale_day['Fecha']}, {max_sale_day['Venta']}\n")
    output.write(f"Día de menor venta: {min_sale_day['Fecha']}, {min_sale_day['Venta']}\n")
    return output.getvalue().encode('utf-8')

def main():
    st.title("Estadísticas de Ventas Diarias")

    uploaded_file = st.file_uploader("Sube tu archivo de ventas diarias (TXT)", type=["txt"])

    if uploaded_file is not None:
        data = read_sales_file(uploaded_file)
        st.write("Datos cargados:")
        st.dataframe(data)

        total_sales, average_sales, max_sale_day, min_sale_day = calculate_statistics(data)

        st.write(f"Venta total: {total_sales}")
        st.write(f"Promedio de ventas: {average_sales}")
        st.write(f"Día de mayor venta: {max_sale_day['Fecha']}, {max_sale_day['Venta']}")
        st.write(f"Día de menor venta: {min_sale_day['Fecha']}, {min_sale_day['Venta']}")

        save_button = st.button("Guardar estadísticas en archivo")

        if save_button:
            output = save_statistics(total_sales, average_sales, max_sale_day, min_sale_day)
            st.download_button(label="Descargar estadísticas",
                               data=output,
                               file_name="estadisticas_ventas.txt",
                               mime="text/plain")
            st.success("Archivo guardado con éxito como 'estadisticas_ventas.txt'.")

if __name__ == "__main__":
    main()
