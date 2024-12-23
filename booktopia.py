import mysql.connector
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print  
from rich.style import Style
from rich.console import Group
import time
import datetime
import pyfiglet
import os

def show_loading(console, message="Memuat data..."):
    console.print("\n")
    with Progress(
        SpinnerColumn("dots", style="yellow"),
        TextColumn(f"[cyan]{message}[/cyan]"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("loading", total=30)
        for _ in range(30):
            time.sleep(0.3)
            progress.update(task, advance=1)

def welcome():
    try:
        ascii_art_booktopia = pyfiglet.figlet_format("BOOKTOPIA", font="chunky")
        terminal_width = os.get_terminal_size().columns

        console = Console() 
        for line in ascii_art_booktopia.split('\n'):
            console.print(line.center(terminal_width), style="magenta")

    except Exception as e:
        print(f"[red]Error in welcome function: {e}[/red]")
    

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="booktopia",
)

def insert_book(connection):
    book_id = input("Masukkan ID Buku : ")
    title = input("Masukkan Judul Buku : ")
    author = input("Masukkan Penulis Buku : ")
    year = input("Masukkan Tahun Terbit : ")
    stock = int(input("Masukkan Stok Buku : "))
    cursor = connection.cursor()

    query = "INSERT INTO books (book_id, title, author, year, stock) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (book_id, title, author, year, stock))
    connection.commit()
    print("{} Data berhasil disimpan".format(cursor.rowcount))
    

def show_books(connection):
    console = Console()
    cursor = connection.cursor()
    sql = "SELECT * FROM books"
    cursor.execute(sql)
    result = cursor.fetchall()

    if cursor.rowcount <= 0:
        console.print("[red]Tidak ada data yang tersedia[/red]")
    else:
        table = Table(title="Daftar Buku", border_style="blue")
        table.add_column("ID Buku", justify="center")
        table.add_column("Judul Buku", justify="left")
        table.add_column("Penulis", justify="left")
        table.add_column("Tahun Terbit", justify="center")
        table.add_column("Stok", justify="center")

        for data in result:
            book_id, title, author, year, stock = data
            if stock < 5:
                stock_color = "[red]{}[/red]".format(stock)
            elif stock < 10:
                stock_color = "[yellow]{}[/yellow]".format(stock)
            elif stock > 15:
                stock_color = "[green]{}[/green]".format(stock)
            else:
                stock_color = str(stock)

            table.add_row(str(book_id), title, author, str(year), stock_color)

        console.print(table)

def update_book(connection):
    cursor = connection.cursor()
    show_books(connection)
    book_id = input("Masukkan ID Buku yang ingin diupdate : ")
    title = input("Masukkan Judul Baru : ")
    author = input("Masukkan Penulis Baru : ")
    year = input("Masukkan Tahun Terbit Baru : ")
    stock = int(input("Masukkan Stok Baru : "))

    sql = "UPDATE books SET title = %s, author = %s, year = %s, stock = %s WHERE book_id = %s"
    cursor.execute(sql, (title, author, year, stock, book_id))
    connection.commit()
    print("{} Data berhasil diubah".format(cursor.rowcount))

def delete_book(connection):
    cursor = connection.cursor()
    show_books(connection)
    book_id = input("Masukkan ID Buku yang ingin dihapus : ")
    sql = "DELETE FROM books WHERE book_id = %s"
    cursor.execute(sql, (book_id,))
    connection.commit()
    print("{} Data berhasil dihapus".format(cursor.rowcount))

def search_books(connection):
    cursor = connection.cursor()
    keyword = input("Kata kunci : ")
    sql = ("SELECT * FROM books WHERE title LIKE %s OR author LIKE %s")
    cursor.execute(sql, ('%' + keyword + '%', '%' + keyword + '%'))
    result = cursor.fetchall()

    console = Console()
    if cursor.rowcount <= 0:
        console.print("[red]Tidak ada data[/red]")
    else:
        table = Table(title="Hasil Pencarian", border_style="green")

        table.add_column("ID Buku", justify="center")
        table.add_column("Judul Buku", justify="left")
        table.add_column("Penulis", justify="left")
        table.add_column("Tahun Terbit", justify="center")
        table.add_column("Stok", justify="center")

        for data in result:
            book_id, title, author, year, stock = data
            if stock < 5:
                stock_color = "[red]{}[/red]".format(stock)
            elif stock < 10:
                stock_color = "[yellow]{}[/yellow]".format(stock)
            elif stock > 15:
                stock_color = "[green]{}[/green]".format(stock)
            else:
                stock_color = str(stock)

            table.add_row(str(book_id), title, author, str(year), stock_color)

        console.print(table)

def insert_pegawai(connection):
    pegawai_id = input("Masukkan ID Pegawai : ")
    name = input("Masukkan Nama Pegawai : ")
    position = input("Masukkan Jabatan Pegawai : ")
    cursor = connection.cursor()

    query = "INSERT INTO pegawai (pegawai_id, name, position) VALUES (%s, %s, %s)"
    cursor.execute(query, (pegawai_id, name, position))
    connection.commit()
    print("{} Data pegawai berhasil disimpan".format(cursor.rowcount))

def show_pegawai(connection):
    cursor = connection.cursor()
    sql = "SELECT * FROM pegawai"
    cursor.execute(sql)
    result = cursor.fetchall()

    console = Console()
    if cursor.rowcount <= 0:
        console.print("[red]Tidak ada data pegawai yang tersedia[/red]")
    else:
        table = Table(title="Daftar Pegawai", border_style="yellow")

        table.add_column("ID Pegawai", justify="center")
        table.add_column("Nama Pegawai", justify="left")
        table.add_column("Jabatan", justify="left")

        for data in result:
            table.add_row(str(data[0]), data[1], data[2])

        console.print(table)

def update_pegawai(connection):
    cursor = connection.cursor()
    show_pegawai(connection)
    pegawai_id = input("Masukkan ID Pegawai yang ingin diupdate : ")
    name = input("Masukkan Nama Baru : ")
    position = input("Masukkan Jabatan Baru : ")

    sql = "UPDATE pegawai SET name = %s, position = %s WHERE pegawai_id = %s"
    cursor.execute(sql, (name, position, pegawai_id))
    connection.commit()
    print("{} Data pegawai berhasil diubah".format(cursor.rowcount))

def delete_pegawai(connection):
    cursor = connection.cursor()
    show_pegawai(connection)
    pegawai_id = input("Masukkan ID Pegawai yang ingin dihapus : ")
    sql = "DELETE FROM pegawai WHERE pegawai_id = %s"
    cursor.execute(sql, (pegawai_id,))
    connection.commit()
    print("{} Data pegawai berhasil dihapus".format(cursor.rowcount))

def search_pegawai(connection):
    cursor = connection.cursor()
    keyword = input("Kata kunci : ")
    sql = ("SELECT * FROM pegawai WHERE name LIKE %s OR position LIKE %s")
    cursor.execute(sql, ('%' + keyword + '%', '%' + keyword + '%'))
    result = cursor.fetchall()

    console = Console()
    if cursor.rowcount <= 0:
        console.print("[red]Tidak ada data pegawai[/red]")
    else:
        table = Table(title="Hasil Pencarian Pegawai", border_style="cyan")

        table.add_column("ID Pegawai", justify="center")
        table.add_column("Nama Pegawai", justify="left")
        table.add_column("Jabatan", justify="left")

        for data in result:
            table.add_row(str(data[0]), data[1], data[2])

        console.print(table)

def insert_peminjaman(connection):
    console = Console()
    borrowed_books = []  
    nama_customer = input("Masukkan Nama Peminjam yang meminjam : ")
    alamat_customer = input("Masukkan Alamat Peminjam : ")

    while True: 
        show_books(connection)  

        book_id = input("Masukkan ID Buku yang dipinjam : ")
        cursor = connection.cursor()
        cursor.execute("SELECT title, stock FROM books WHERE book_id = %s", (book_id,))
        book_result = cursor.fetchone()

        if book_result:
            nama_buku, stock = book_result
            if stock <= 0:
                console.print("[red]Stok buku tidak tersedia untuk peminjaman.[/red]")
                return

            tanggal_pinjam = datetime.datetime.now()
            tanggal_kembali_input = input("Masukkan Tanggal Pengembalian (YYYY-MM-DD) : ")
            
            try:
                tanggal_kembali = datetime.datetime.strptime(tanggal_kembali_input, "%Y-%m-%d")
                if tanggal_kembali < tanggal_pinjam:
                    console.print("[red]Tanggal pengembalian tidak boleh sebelum tanggal peminjaman.[/red]")
                    return
            except ValueError:
                console.print("[red]Format tanggal tidak valid. Harap masukkan dalam format YYYY-MM-DD.[/red]")
                return

            query = "INSERT INTO peminjaman (book_id, nama_customer, alamat_customer, nama_buku, tanggal_pinjam, tanggal_kembali) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (book_id, nama_customer, alamat_customer, nama_buku, tanggal_pinjam, tanggal_kembali))
            connection.commit()

            new_stock = stock - 1
            update_stock_query = "UPDATE books SET stock = %s WHERE book_id = %s"
            cursor.execute(update_stock_query, (new_stock, book_id))
            connection.commit()

            borrowed_books.append((nama_buku, tanggal_kembali.strftime('%Y-%m-%d')))  
            console.print("{} Data jaman untuk '{}' berhasil disimpan".format(cursor.rowcount, nama_buku))

        else:
            console.print("[red]ID Buku tidak ditemukan[/red]")

        another = input("Apakah Anda ingin menambah pinjaman buku lagi? (y/n): ")
        if another.lower() != 'y':
            break  

    ascii_art_small_header = pyfiglet.figlet_format("Booktopia", font="chunky")
    
    receipt_panel = Panel.fit(
        f"[magenta]{ascii_art_small_header}[/magenta]\n" 
        f"Tanggal      : {tanggal_pinjam.strftime('%Y-%m-%d')}\n"
        f"Waktu        : {tanggal_pinjam.strftime('%H:%M:%S')}\n"
        f"Nama Peminjam: {nama_customer}\n"
        f"Alamat       : {alamat_customer}\n\n"
        f"[bold]Daftar Buku yang Dipinjam:[/bold]\n"
    )

    for buku, tanggal_kembali in borrowed_books:
        receipt_panel.renderable += f"- {buku} (Tanggal Pengembalian: {tanggal_kembali})\n"

    receipt_panel.renderable += "\n[bold yellow]Terima kasih telah meminjam buku di perpustakaan Booktopia![/bold yellow]"
    console.print(receipt_panel)

    show_peminjaman_menu(connection)

def show_peminjaman(connection):
    cursor = connection.cursor()
    sql = "SELECT * FROM peminjaman"
    cursor.execute(sql)
    result = cursor.fetchall()

    console = Console()
    if cursor.rowcount <= 0:
        console.print("[red]Tidak ada data peminjaman yang tersedia[/red]")
    else:
        table = Table(title="Daftar Peminjaman", border_style="yellow")

        table.add_column("ID Peminjaman", justify="center", style="cyan")
        table.add_column("ID Buku", justify="center", style="cyan")
        table.add_column("Nama Customer", justify="left", style="cyan")
        table.add_column("Alamat Customer", justify="left", style="cyan")  
        table.add_column("Nama Buku", justify="left", style="cyan")
        table.add_column("Tanggal Peminjaman", justify="center", style="cyan")
        table.add_column("Tanggal Pengembalian", justify="center", style="cyan")

        for data in result:
            table.add_row(str(data[0]), str(data[1]), data[2], data[3], str(data[4]), str(data[5]), str(data[6]))

        console.print(table)

def delete_peminjaman(connection):
    cursor = connection.cursor()
    show_peminjaman(connection)
    peminjaman_id = input("Masukkan ID Peminjaman yang ingin dihapus : ")
    sql = "DELETE FROM peminjaman WHERE peminjaman_id = %s"
    cursor.execute(sql, (peminjaman_id,))
    connection.commit()
    print("{} Data peminjaman berhasil dihapus".format(cursor.rowcount))

def show_book_menu(connection):
    console = Console()
    while True:
        
        panel_content = """\
    Tambah Buku
    Tampilkan Buku
    Update Buku
    Cari Buku
    Hapus Buku
    Kembali ke Menu Utama
"""
        menu_items = [f"[[bold cyan]{index}[/bold cyan]] [magenta]{item.strip()}[/magenta]" for index, item in enumerate(panel_content.splitlines(), start=1) if item.strip()]
        menu = "\n".join(menu_items)  

        console.print(Panel.fit(menu, title="Menu Buku", title_align="center", border_style="bright_blue", padding=(1, 4)))

        menu_input = input("Pilih Menu (masukkan nomor): ") 
        if menu_input in [str(i) for i in range(len(menu_items) + 1)]:

            if menu_input == "1":
                insert_book(connection)

            elif menu_input == "2":
                show_books(connection)
        
            elif menu_input == "3":
                update_book(connection)
        
            elif menu_input == "4":
                search_books(connection)
        
            elif menu_input == "5":
                delete_book(connection)
        
            elif menu_input == "6":
                return  
        
        else:
            console.print("[red]Menu tidak tersedia[/red]")

        

def show_menu_pegawai(connection):
    console = Console()
    while True:
        
        panel_content = """\
    Tambah Pegawai
    Tampilkan Pegawai
    Update Pegawai
    Cari Pegawai
    Hapus Pegawai
    Kembali ke Menu Utama
"""
        menu_items = [f"[[bold cyan]{index}[/bold cyan]] [magenta]{item.strip()}[/magenta]" for index, item in enumerate(panel_content.splitlines(), start=1) if item.strip()]
        menu = "\n".join(menu_items)  

        console.print(Panel.fit(menu, title="Menu Pegawai", title_align="center", border_style="bright_blue", padding=(1, 4)))

        menu_input = input("Pilih Menu (masukkan nomor): ") 
        if menu_input in [str(i) for i in range(len(menu_items) + 1)]:

            if menu_input == "1":
                insert_pegawai(connection)

            elif menu_input == "2":
                show_pegawai(connection)
        
            elif menu_input == "3":
                update_pegawai(connection)
        
            elif menu_input == "4":
                search_pegawai(connection)
        
            elif menu_input == "5":
                delete_pegawai(connection)
        
            elif menu_input == "6":
                return  
        
        else:
            console.print(Panel("Menu tidak tersedia", style="red"))
def show_peminjaman_menu(connection):
    console = Console()
    while True:
        panel_content = """\
    Tambah Peminjaman
    Tampilkan Peminjaman
    Hapus Peminjaman
    Kembali ke Menu Utama
"""
        menu_items = [f"[[bold cyan]{index}[/bold cyan]] [magenta]{item.strip()}[/magenta]" for index, item in enumerate(panel_content.splitlines(), start=1) if item.strip()]
        menu = "\n".join(menu_items)  

        console.print(Panel.fit(menu, title="Menu Peminjaman", title_align="center", border_style="bright_blue", padding=(1, 4)))

        menu_input = input("Pilih Menu (masukkan nomor): ")  
        if menu_input in [str(i) for i in range(len(menu_items) + 1)]:
            
            if menu_input == '1':
                insert_peminjaman(connection)
            elif menu_input == '2':
                show_peminjaman(connection)
            elif menu_input == '3':
                delete_peminjaman(connection)
            elif menu_input == '4':
                break  
        else:
            console.print("[red]Pilihan tidak valid. Silakan coba lagi.[/red]")

def return_book(connection):
    console = Console()
    show_peminjaman(connection)
    peminjaman_id = input("Masukkan ID Peminjaman yang ingin dikembalikan : ")
    cursor = connection.cursor()

    cursor.execute("SELECT book_id FROM peminjaman WHERE peminjaman_id = %s", (peminjaman_id,))
    result = cursor.fetchone()

    if result:
        book_id = result[0]
        cursor.execute("DELETE FROM peminjaman WHERE peminjaman_id = %s", (peminjaman_id,))
        connection.commit()

        cursor.execute("SELECT stock FROM books WHERE book_id = %s", (book_id,))
        stock_result = cursor.fetchone()
        if stock_result:
            new_stock = stock_result[0] + 1
            cursor.execute("UPDATE books SET stock = %s WHERE book_id = %s", (new_stock, book_id))
            connection.commit()

        console.print("[green]Buku berhasil dikembalikan.[/green]")
    else:
        console.print("[red]ID Peminjaman tidak ditemukan.[/red]")

def show_menu(connection):
    try:
        console = Console()
        show_loading(console, "Sedang memuat Booktopia...")
        welcome()
        
    except Exception as e:
        print(f"[red]Error in show_menu function: {e}[/red]")
    
    text = """\n\n[#ffa45e]====== WELCOME TO BOOKTOPIA ======[/#ffa45e]\n\n"""
    menu_list = ["Buku", "Pegawai", "Peminjaman", "Pengembalian", "Log Out"]

    console.print(text)
    while True:
        menu = "\n".join(
            [f"[[bold cyan]{index}[/bold cyan]] [magenta]{item}[/magenta]" for index, item in enumerate(menu_list, start=1)]
        )
        console.print(Panel.fit(menu, title="Main Menu", title_align="center", border_style="bright_blue", padding=(1, 4)))

        try:
            user_input = int(input("Masukkan pilihan: "))
            if user_input == 1:
                show_book_menu(connection)  

            elif user_input == 2:
                show_menu_pegawai(connection)  
        
            elif user_input == 3:
                show_peminjaman_menu(connection)  

            elif user_input == 4:
                return_book(connection)  

            elif user_input == 5:
                print("[bold yellow]Terima kasih telah berkunjung ke perpustakaan Booktopia![/bold yellow]")
                exit()  
        
            else:
                print("Menu tidak tersedia")

        except ValueError:
            print("Input tidak valid, silakan masukkan angka yang sesuai.")
            
if __name__ == "__main__" :
    while(True) :
        show_menu(connection)
