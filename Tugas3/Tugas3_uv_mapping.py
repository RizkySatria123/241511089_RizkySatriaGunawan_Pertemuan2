import bpy
import os

def main():
    # --- 1. PERSIAPAN OBJEK ---
    # Daftar nama objek kursi Anda dari screenshot
    obj_names = ["Cube", "Cube.001", "Cube.002", "Cube.003", "Cube.004", "Cube.005"]
    
    chair_parts = []
    for name in obj_names:
        if name in bpy.data.objects:
            obj = bpy.data.objects[name]
            chair_parts.append(obj)
            # Pastikan objek terlihat dan bisa dipilih
            obj.hide_set(False)
            obj.hide_select = False
        else:
            print(f"Peringatan: Objek '{name}' tidak ditemukan.")

    if not chair_parts:
        print("Error: Tidak ada objek kursi yang ditemukan. Pastikan nama objek sesuai.")
        return

    # Deselect semua objek terlebih dahulu
    bpy.ops.object.select_all(action='DESELECT')

    # Pilih semua bagian kursi dan jadikan satu objek aktif
    bpy.context.view_layer.objects.active = chair_parts[0]
    for obj in chair_parts:
        obj.select_set(True)

    # Gabungkan semua bagian menjadi "1 objek kompleks"
    print("Menggabungkan bagian-bagian kursi...")
    bpy.ops.object.join()
    
    # Objek yang baru digabung sekarang adalah objek aktif
    obj = bpy.context.active_object
    obj.name = "Kursi_Kompleks"
    
    # --- 2. UV UNWRAPPING (OTOMATIS) ---
    print("Memulai proses Smart UV Project (Unwrap & Pack)...")
    # Masuk ke Edit Mode
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Pilih semua mesh
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Lakukan Smart UV Project (ini sudah termasuk Unwrap dan basic Pack)
    bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.01)
    
    print("Proses Unwrap selesai.")

    # --- 3. EXPORT UV LAYOUT ---
    print("Mengekspor UV layout...")
    
    # Tentukan path file di sebelah file .blend Anda
    if not bpy.data.filepath:
        print("Error: Harap simpan file .blend Anda terlebih dahulu sebelum mengekspor UV.")
        bpy.ops.object.mode_set(mode='OBJECT')
        return

    directory = os.path.dirname(bpy.data.filepath)
    export_path = os.path.join(directory, "kursi_uv_layout.png")

    # Ekspor UV layout
    bpy.ops.uv.export_layout(filepath=export_path, size=(1024, 1024), opacity=0.8)
    print(f"UV Layout telah diekspor ke: {export_path}")

    # --- 4. APPLY DEFAULT MATERIAL (TANPA TEXTURE) ---
    print("Menerapkan material default (abu-abu)...")
    # Kembali ke Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Buat material baru
    mat = bpy.data.materials.new(name="Material_Default")
    obj.data.materials.clear() # Hapus material lama
    obj.data.materials.append(mat)
    
    # Gunakan nodes
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Bersihkan node (jika ada node default)
    nodes.clear()

    # Buat node output
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    output_node.location = (200, 0)
    
    # Buat node shader (Principled BSDF) - ini akan jadi abu-abu default
    shader_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    shader_node.location = (0, 0)
    
    # Hubungkan shader ke output
    links.new(shader_node.outputs['BSDF'], output_node.inputs['Surface'])
    
    # Bagian Image Texture dan UV Grid telah dihapus

    print("--- Selesai ---")
    print("Objek telah di-unwrap dan diberi material default.")

# Jalankan fungsi utama
main()