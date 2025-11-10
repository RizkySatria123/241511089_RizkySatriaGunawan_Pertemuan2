import bpy

def set_object_mode():
    """Memastikan Blender berada di Object Mode"""
    if bpy.context.object and bpy.context.object.mode == 'EDIT':
        bpy.ops.object.mode_set(mode='OBJECT')

def create_advanced_shader_group():
    """
    Membuat Node Group 'Tugas4_Worn_PBR' yang reusable.
    """
    print("Membuat Node Group 'Tugas4_Worn_PBR'...")
    
    # 1. Buat Node Group baru
    group = bpy.data.node_groups.new(name="Tugas4_Worn_PBR", type='ShaderNodeTree')

    # 2. Definisikan Input untuk Group
    group.interface.new_socket(name="Base Color", in_out='INPUT', socket_type='NodeSocketColor')
    group.interface.new_socket(name="Dirt Color", in_out='INPUT', socket_type='NodeSocketColor')
    group.interface.new_socket(name="Edge Glow Color", in_out='INPUT', socket_type='NodeSocketColor')
    
    noise_scale_socket = group.interface.new_socket(name="Noise Scale", in_out='INPUT', socket_type='NodeSocketFloat')
    noise_scale_socket.default_value = 5.0
    
    noise_strength_socket = group.interface.new_socket(name="Noise Strength", in_out='INPUT', socket_type='NodeSocketFloat')
    noise_strength_socket.default_value = 0.5
    
    roughness_socket = group.interface.new_socket(name="Base Roughness", in_out='INPUT', socket_type='NodeSocketFloat')
    roughness_socket.default_value = 0.5
    
    fresnel_socket = group.interface.new_socket(name="Fresnel Blend", in_out='INPUT', socket_type='NodeSocketFloat')
    fresnel_socket.default_value = 0.5

    # 3. Definisikan Output untuk Group
    group.interface.new_socket(name="Base Color Out", in_out='OUTPUT', socket_type='NodeSocketColor')
    group.interface.new_socket(name="Roughness Out", in_out='OUTPUT', socket_type='NodeSocketFloat')
    group.interface.new_socket(name="Normal Out", in_out='OUTPUT', socket_type='NodeSocketVector')

    # 4. Buat Node Internal
    nodes = group.nodes

    group_input = next((n for n in nodes if n.type == 'GROUP_INPUT'), None)
    if not group_input:
        group_input = nodes.new('NodeGroupInput')

    group_output = next((n for n in nodes if n.type == 'GROUP_OUTPUT'), None)
    if not group_output:
        group_output = nodes.new('NodeGroupOutput')

    group_input.location = (-1000, 0)
    group_output.location = (600, 0)

    # Teknik 1: Bump/Normal Mapping
    noise_tex = nodes.new('ShaderNodeTexNoise')
    noise_tex.location = (-650, -320)
    noise_tex.inputs['Detail'].default_value = 5.5
    noise_tex.inputs['Roughness'].default_value = 0.45

    noise_ramp = nodes.new('ShaderNodeValToRGB')
    noise_ramp.location = (-420, -340)
    noise_ramp.label = "Noise Contrast"
    noise_ramp.color_ramp.elements[0].position = 0.25
    noise_ramp.color_ramp.elements[1].position = 0.75
    
    bump_node = nodes.new('ShaderNodeBump')
    bump_node.location = (-100, -320)
    bump_node.inputs['Distance'].default_value = 0.2

    # Teknik 2: Ambient Occlusion (Dirt Mask)
    ao_node = nodes.new('ShaderNodeAmbientOcclusion')
    ao_node.location = (-650, 20)
    ao_node.samples = 16 
    ao_node.inputs['Distance'].default_value = 2.0
    
    ao_noise_mask = nodes.new('ShaderNodeMath')
    ao_noise_mask.operation = 'MULTIPLY'
    ao_noise_mask.location = (-120, -40)
    ao_noise_mask.inputs[1].default_value = 1.0
    ao_noise_mask.use_clamp = True

    mask_strength = nodes.new('ShaderNodeMath')
    mask_strength.operation = 'MULTIPLY'
    mask_strength.location = (120, -40)
    mask_strength.inputs[1].default_value = 1.0
    mask_strength.use_clamp = True
    
    mix_dirt = nodes.new('ShaderNodeMix') 
    mix_dirt.location = (-300, 0)
    mix_dirt.data_type = 'RGBA' 
    mix_dirt.blend_type = 'MIX'
    
    # Teknik 3: Layer Weight (Fresnel/Edge Glow)
    layer_weight = nodes.new('ShaderNodeLayerWeight')
    layer_weight.location = (-600, 300)

    color_ramp = nodes.new('ShaderNodeValToRGB') 
    color_ramp.location = (-300, 300)
    color_ramp.color_ramp.elements[0].position = 0.55
    color_ramp.color_ramp.elements[1].position = 0.95
    
    mix_edge = nodes.new('ShaderNodeMix')
    mix_edge.location = (0, 150)
    mix_edge.data_type = 'RGBA'
    mix_edge.blend_type = 'ADD' 
    
    roughness_variance = nodes.new('ShaderNodeMath')
    roughness_variance.operation = 'MULTIPLY'
    roughness_variance.location = (120, -260)
    roughness_variance.inputs[1].default_value = 0.6
    roughness_variance.use_clamp = True

    roughness_boost = nodes.new('ShaderNodeMath')
    roughness_boost.operation = 'ADD'
    roughness_boost.location = (320, -260)
    roughness_boost.use_clamp = True

    roughness_mix = nodes.new('ShaderNodeMix')
    roughness_mix.location = (520, -220)
    roughness_mix.data_type = 'FLOAT'
    roughness_mix.blend_type = 'MIX'
    roughness_mix.clamp_result = True
    
    # 5. Hubungkan Node (Linking)
    links = group.links
    
    links.new(group_input.outputs['Base Color'], mix_dirt.inputs['A'])
    links.new(group_input.outputs['Dirt Color'], mix_dirt.inputs['B'])
    links.new(group_input.outputs['Noise Scale'], noise_tex.inputs['Scale'])
    links.new(group_input.outputs['Noise Strength'], bump_node.inputs['Strength'])
    links.new(group_input.outputs['Edge Glow Color'], mix_edge.inputs['B'])
    links.new(group_input.outputs['Fresnel Blend'], layer_weight.inputs['Blend'])

    links.new(noise_tex.outputs['Fac'], noise_ramp.inputs['Fac'])
    links.new(noise_ramp.outputs['Color'], ao_noise_mask.inputs[1])
    links.new(ao_node.outputs['AO'], ao_noise_mask.inputs[0])
    links.new(ao_noise_mask.outputs['Value'], mask_strength.inputs[0])
    links.new(group_input.outputs['Noise Strength'], mask_strength.inputs[1])
    links.new(mask_strength.outputs['Value'], mix_dirt.inputs['Factor']) 
    links.new(mask_strength.outputs['Value'], roughness_mix.inputs['Factor'])
    links.new(noise_tex.outputs['Fac'], bump_node.inputs['Height']) 

    links.new(layer_weight.outputs['Fresnel'], color_ramp.inputs['Fac']) 
    links.new(color_ramp.outputs['Color'], mix_edge.inputs['Factor']) 
    links.new(mix_dirt.outputs['Result'], mix_edge.inputs['A']) 

    links.new(mask_strength.outputs['Value'], roughness_variance.inputs[0])
    links.new(roughness_variance.outputs['Value'], roughness_boost.inputs[1])
    links.new(group_input.outputs['Base Roughness'], roughness_boost.inputs[0])
    links.new(group_input.outputs['Base Roughness'], roughness_mix.inputs['A'])
    links.new(roughness_boost.outputs['Value'], roughness_mix.inputs['B'])

    links.new(mix_edge.outputs['Result'], group_output.inputs['Base Color Out'])
    links.new(roughness_mix.outputs['Result'], group_output.inputs['Roughness Out'])
    links.new(bump_node.outputs['Normal'], group_output.inputs['Normal Out'])
    return group


def create_materials(node_group_name="Tugas4_Worn_PBR"):
    """
    Membuat 3 material berbeda menggunakan Node Group yang sama.
    """
    print("Membuat 3 material...")
    
    if node_group_name not in bpy.data.node_groups:
        print(f"Error: Node Group '{node_group_name}' tidak ditemukan.")
        return

    material_specs = [
        {"name": "Material_Karat", "base_color": (0.8, 0.2, 0.0, 1), "dirt_color": (0.1, 0.05, 0.0, 1), "edge_color": (0.9, 0.4, 0.1, 1), "noise_scale": 15.0, "noise_strength": 0.8, "roughness": 0.85, "fresnel_blend": 0.7},
        {"name": "Material_Plastik_Baru", "base_color": (0.05, 0.2, 0.8, 1), "dirt_color": (0.01, 0.01, 0.01, 1), "edge_color": (0.5, 0.7, 1.0, 1), "noise_scale": 5.0, "noise_strength": 0.1, "roughness": 0.2, "fresnel_blend": 0.3},
        {"name": "Material_Keramik", "base_color": (0.9, 0.9, 0.9, 1), "dirt_color": (0.2, 0.1, 0.1, 1), "edge_color": (1.0, 1.0, 1.0, 1), "noise_scale": 50.0, "noise_strength": 0.05, "roughness": 0.1, "fresnel_blend": 0.1}
    ]

    materials = []
    for spec in material_specs:
        mat = bpy.data.materials.new(name=spec["name"])
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear() 

        output_node = nodes.new('ShaderNodeOutputMaterial')
        output_node.location = (400, 0)
        
        shader_node = nodes.new('ShaderNodeBsdfPrincipled')
        shader_node.location = (100, 0)
        
        links.new(shader_node.outputs['BSDF'], output_node.inputs['Surface'])

        group_node = nodes.new('ShaderNodeGroup')
        group_node.node_tree = bpy.data.node_groups[node_group_name]
        group_node.location = (-300, 0)

        group_node.inputs["Base Color"].default_value = spec["base_color"]
        group_node.inputs["Dirt Color"].default_value = spec["dirt_color"]
        group_node.inputs["Edge Glow Color"].default_value = spec["edge_color"]
        group_node.inputs["Noise Scale"].default_value = spec["noise_scale"]
        group_node.inputs["Noise Strength"].default_value = spec["noise_strength"]
        group_node.inputs["Base Roughness"].default_value = spec["roughness"]
        group_node.inputs["Fresnel Blend"].default_value = spec["fresnel_blend"]
        
        links.new(group_node.outputs['Base Color Out'], shader_node.inputs['Base Color'])
        links.new(group_node.outputs['Roughness Out'], shader_node.inputs['Roughness'])
        links.new(group_node.outputs['Normal Out'], shader_node.inputs['Normal'])
        
        materials.append(mat)
        print(f"Material '{spec['name']}' berhasil dibuat.")
        
    return materials

def setup_scene(materials):
    """
    Membersihkan scene dan membuat 3 objek untuk menampilkan material.
    """
    print("Menyiapkan scene...")
    
    # --- PERBAIKAN PENTING ---
    set_object_mode()
    
    # Hapus semua MESH objek yang ada (termasuk Kubus default)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    bpy.ops.mesh.primitive_uv_sphere_add(location=(-3, 0, 0))
    sphere = bpy.context.active_object
    bpy.ops.object.shade_smooth() 

    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
    cube = bpy.context.active_object
    
    bpy.ops.mesh.primitive_monkey_add(location=(3, 0, 0))
    monkey = bpy.context.active_object
    bpy.ops.object.shade_smooth() 

    if materials:
        if len(materials) >= 3:
            sphere.data.materials.append(materials[0]) # Material_Karat
            cube.data.materials.append(materials[1]) # Material_Plastik_Baru
            monkey.data.materials.append(materials[2]) # Material_Keramik
        else:
            print("Jumlah material yang dibuat kurang dari 3.")

    print("Scene setup selesai.")


# --- FUNGSI UTAMA UNTUK DIJALANKAN ---

print("--- MEMULAI SKRIP TUGAS 4 ---")

# --- PERBAIKAN PENTING ---
# Pastikan kita di Object Mode sebelum mencoba menghapus apapun
set_object_mode()

if "Tugas4_Worn_PBR" in bpy.data.node_groups:
    bpy.data.node_groups.remove(bpy.data.node_groups["Tugas4_Worn_PBR"])
    
for mat_name in ["Material_Karat", "Material_Plastik_Baru", "Material_Keramik"]:
    if mat_name in bpy.data.materials:
        bpy.data.materials.remove(bpy.data.materials[mat_name])

node_group = create_advanced_shader_group()
if node_group: 
    materials = create_materials(node_group.name)
    setup_scene(materials)

    print("\n--- SKRIP SELESAI ---")
    print("3 objek baru telah dibuat.")
    print("Silakan ganti Viewport Shading ke 'Material Preview' untuk melihat hasilnya.")
else:
    print("\n--- SKRIP GAGAL ---")
    print("Pembuatan node group gagal. Skrip dihentikan.")