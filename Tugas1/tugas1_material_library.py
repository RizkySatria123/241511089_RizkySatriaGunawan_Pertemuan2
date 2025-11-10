import bpy

# 1. Bersihkan Scene (hapus semua objek)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for block in bpy.data.meshes:
    bpy.data.meshes.remove(block)
for block in bpy.data.materials:
    bpy.data.materials.remove(block)

# 2. Membuat 5 Material Kustom (Node-Based)

# a. Material Logam Tembaga/Berkarat
mat_logam_tembaga = bpy.data.materials.new(name="mat_logam_tembaga")
mat_logam_tembaga.use_nodes = True
nodes = mat_logam_tembaga.node_tree.nodes
links = mat_logam_tembaga.node_tree.links
nodes.clear()

mat_out = nodes.new('ShaderNodeOutputMaterial')
mat_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
mat_bsdf.location = (-200, 0)
mat_bsdf.inputs['Metallic'].default_value = 1.0
mat_bsdf.inputs['Roughness'].default_value = 0.5

noise = nodes.new('ShaderNodeTexNoise')
noise.location = (-600, 100)
noise.inputs['Scale'].default_value = 8.0

colorramp = nodes.new('ShaderNodeValToRGB')
colorramp.location = (-400, 100)
colorramp.color_ramp.elements[0].color = (0.72, 0.43, 0.26, 1)   # Copper
colorramp.color_ramp.elements[1].color = (0.4, 0.27, 0.15, 1)    # Oxidized

bump = nodes.new('ShaderNodeBump')
bump.location = (-400, -50)
links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
links.new(colorramp.outputs['Color'], mat_bsdf.inputs['Base Color'])
links.new(noise.outputs['Fac'], bump.inputs['Height'])
links.new(bump.outputs['Normal'], mat_bsdf.inputs['Normal'])
links.new(mat_bsdf.outputs['BSDF'], mat_out.inputs['Surface'])

# b. Material Kain Denim
mat_kain_denim = bpy.data.materials.new(name="mat_kain_denim")
mat_kain_denim.use_nodes = True
nodes = mat_kain_denim.node_tree.nodes
links = mat_kain_denim.node_tree.links
nodes.clear()

mat_out = nodes.new('ShaderNodeOutputMaterial')
mat_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
mat_bsdf.location = (-200, 0)
mat_bsdf.inputs['Roughness'].default_value = 0.85

wave = nodes.new('ShaderNodeTexWave')
wave.location = (-600, 100)
wave.inputs['Scale'].default_value = 30.0
wave.inputs['Distortion'].default_value = 7.5

colorramp = nodes.new('ShaderNodeValToRGB')
colorramp.location = (-400, 100)
colorramp.color_ramp.elements[0].color = (0.1, 0.14, 0.25, 1)   # Denim dark blue
colorramp.color_ramp.elements[1].color = (0.25, 0.30, 0.45, 1)  # Denim highlight

bump = nodes.new('ShaderNodeBump')
bump.location = (-400, -50)
links.new(wave.outputs['Color'], colorramp.inputs['Fac'])
links.new(colorramp.outputs['Color'], mat_bsdf.inputs['Base Color'])
links.new(wave.outputs['Color'], bump.inputs['Height'])
links.new(bump.outputs['Normal'], mat_bsdf.inputs['Normal'])
links.new(mat_bsdf.outputs['BSDF'], mat_out.inputs['Surface'])

# c. Material Organik Kulit Kayu (ganti Musgrave dengan Noise)
mat_organik_kulitkayu = bpy.data.materials.new(name="mat_organik_kulitkayu")
mat_organik_kulitkayu.use_nodes = True
nodes = mat_organik_kulitkayu.node_tree.nodes
links = mat_organik_kulitkayu.node_tree.links
nodes.clear()

mat_out = nodes.new('ShaderNodeOutputMaterial')
mat_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
mat_bsdf.location = (-200, 0)
mat_bsdf.inputs['Roughness'].default_value = 0.7

noise = nodes.new('ShaderNodeTexNoise')
noise.location = (-600, 100)
noise.inputs['Scale'].default_value = 10.0

colorramp = nodes.new('ShaderNodeValToRGB')
colorramp.location = (-400, 100)
colorramp.color_ramp.elements[0].color = (0.27, 0.15, 0.05, 1)   # Bark brown
colorramp.color_ramp.elements[1].color = (0.48, 0.36, 0.23, 1)   # Lighter bark

bump = nodes.new('ShaderNodeBump')
bump.location = (-400, -50)
links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
links.new(colorramp.outputs['Color'], mat_bsdf.inputs['Base Color'])
links.new(noise.outputs['Fac'], bump.inputs['Height'])
links.new(bump.outputs['Normal'], mat_bsdf.inputs['Normal'])
links.new(mat_bsdf.outputs['BSDF'], mat_out.inputs['Surface'])

# d. Material Transparan Batu Giok
mat_trans_jade = bpy.data.materials.new(name="mat_trans_jade")
mat_trans_jade.use_nodes = True
nodes = mat_trans_jade.node_tree.nodes
links = mat_trans_jade.node_tree.links
nodes.clear()

mat_out = nodes.new('ShaderNodeOutputMaterial')
mat_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
mat_bsdf.location = (-200, 0)
mat_bsdf.inputs['IOR'].default_value = 1.55
mat_bsdf.inputs['Roughness'].default_value = 0.1
mat_bsdf.inputs['Base Color'].default_value = (0.18, 0.63, 0.25, 0.7) # Optional transparan dengan alpha


noise = nodes.new('ShaderNodeTexNoise')
noise.location = (-600, 100)
noise.inputs['Scale'].default_value = 20.0

colorramp = nodes.new('ShaderNodeValToRGB')
colorramp.location = (-400, 100)
colorramp.color_ramp.elements[0].color = (0.18, 0.63, 0.25, 1) # Jade base
colorramp.color_ramp.elements[1].color = (0.83, 0.95, 0.65, 1) # Jade highlight

links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
links.new(colorramp.outputs['Color'], mat_bsdf.inputs['Base Color'])
links.new(mat_bsdf.outputs['BSDF'], mat_out.inputs['Surface'])

# e. Material Emisif Lava/Neon
mat_emisif_lava = bpy.data.materials.new(name="mat_emisif_lava")
mat_emisif_lava.use_nodes = True
nodes = mat_emisif_lava.node_tree.nodes
links = mat_emisif_lava.node_tree.links
nodes.clear()

mat_out = nodes.new('ShaderNodeOutputMaterial')
mat_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
mat_bsdf.location = (-200, 60)
mat_bsdf.inputs['Roughness'].default_value = 0.8

emiss = nodes.new('ShaderNodeEmission')
emiss.location = (-200, -80)
emiss.inputs['Strength'].default_value = 10.0

noise = nodes.new('ShaderNodeTexNoise')
noise.location = (-600, 0)
noise.inputs['Scale'].default_value = 10.0

colorramp = nodes.new('ShaderNodeValToRGB')
colorramp.location = (-400, -80)
colorramp.color_ramp.elements[0].color = (1, 0.1, 0, 1)   # Lava hot (red/orange)
colorramp.color_ramp.elements[1].color = (0, 0, 0, 1)     # Lava cold (black)

mixshader = nodes.new('ShaderNodeMixShader')
mixshader.location = (0, 0)

links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
links.new(colorramp.outputs['Color'], emiss.inputs['Color'])
links.new(noise.outputs['Fac'], mat_bsdf.inputs['Base Color'])
links.new(emiss.outputs['Emission'], mixshader.inputs[1])
links.new(mat_bsdf.outputs['BSDF'], mixshader.inputs[2])
links.new(noise.outputs['Fac'], mixshader.inputs['Fac'])
links.new(mixshader.outputs['Shader'], mat_out.inputs['Surface'])

# 3. Membuat Objek Mesh Primitif

objs = []
# Sphere
bpy.ops.mesh.primitive_uv_sphere_add(location=(0,0,0))
obj1 = bpy.context.active_object
objs.append(obj1)
# Cube
bpy.ops.mesh.primitive_cube_add(location=(3,0,0))
obj2 = bpy.context.active_object
objs.append(obj2)
# Cylinder
bpy.ops.mesh.primitive_cylinder_add(location=(6,0,0))
obj3 = bpy.context.active_object
objs.append(obj3)
# Torus
bpy.ops.mesh.primitive_torus_add(location=(9,0,0))
obj4 = bpy.context.active_object
objs.append(obj4)
# Monkey
bpy.ops.mesh.primitive_monkey_add(location=(12,0,0))
obj5 = bpy.context.active_object
objs.append(obj5)

# 4. Terapkan 1 Material unik pada setiap objek
obj1.data.materials.append(mat_kain_denim)          # Sphere: Denim
obj2.data.materials.append(mat_logam_tembaga)       # Cube: Tembaga
obj3.data.materials.append(mat_organik_kulitkayu)   # Cylinder: Kulit Kayu
obj4.data.materials.append(mat_trans_jade)          # Torus: Giok
obj5.data.materials.append(mat_emisif_lava)         # Monkey: Lava

print("Berhasil membuat dan menerapkan 5 material kustom pada 5 objek berbeda.")
