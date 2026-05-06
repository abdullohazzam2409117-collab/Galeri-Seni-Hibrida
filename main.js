// File JavaScript utama untuk interaksi antarmuka
console.log("Aset JavaScript berhasil dimuat melalui url_for");

// Contoh interaksi sederhana: konfirmasi hapus yang lebih cantik
document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if(!confirm('Apakah Anda yakin ingin menghapus data ini?')) {
                e.preventDefault();
            }
        });
    });
});
