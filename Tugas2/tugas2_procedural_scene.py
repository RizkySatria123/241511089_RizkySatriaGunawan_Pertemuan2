import bpy
import math

# Bersihkan scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for block in bpy.data.meshes:
    bpy.data.meshes.remove(block)
for block in bpy.data.materials:
    bpy.data.materials.remove(block)

# (Material definitions tetap sama)

def mat_ground_soil(name):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    n = m.node_tree.nodes
    l = m.node_tree.links
    n.clear()
    out = n.new('ShaderNodeOutputMaterial')
    principled = n.new('ShaderNodeBsdfPrincipled')
    noise = n.new('ShaderNodeTexNoise')
    colorramp = n.new('ShaderNodeValToRGB')
    bump = n.new('ShaderNodeBump')
    disp = n.new('ShaderNodeDisplacement')
    noise.inputs['Scale'].default_value = 8.5
    colorramp.color_ramp.elements[0].color = (0.2,0.13,0.08,1)
    colorramp.color_ramp.elements[1].color = (0.3,0.22,0.12,1)
    l.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
    l.new(colorramp.outputs['Color'], principled.inputs['Base Color'])
    l.new(noise.outputs['Fac'], bump.inputs['Height'])
    l.new(bump.outputs['Normal'], principled.inputs['Normal'])
    l.new(noise.outputs['Fac'], disp.inputs['Height'])
    l.new(disp.outputs['Displacement'], out.inputs['Displacement'])
    l.new(principled.outputs['BSDF'], out.inputs['Surface'])
    return m

def mat_stone(name):
    # sama seperti sebelumnya
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    n = m.node_tree.nodes
    l = m.node_tree.links
    n.clear()
    out = n.new('ShaderNodeOutputMaterial')
    principled = n.new('ShaderNodeBsdfPrincipled')
    voronoi = n.new('ShaderNodeTexVoronoi')
    colorramp = n.new('ShaderNodeValToRGB')
    bump = n.new('ShaderNodeBump')
    voronoi.distance = 'EUCLIDEAN'
    voronoi.inputs['Scale'].default_value = 22.0
    colorramp.color_ramp.elements[0].color = (0.22,0.23,0.22,1)
    colorramp.color_ramp.elements[1].color = (0.5,0.49,0.45,1)
    l.new(voronoi.outputs['Distance'], colorramp.inputs['Fac'])
    l.new(colorramp.outputs['Color'], principled.inputs['Base Color'])
    l.new(voronoi.outputs['Distance'], bump.inputs['Height'])
    l.new(bump.outputs['Normal'], principled.inputs['Normal'])
    l.new(principled.outputs['BSDF'], out.inputs['Surface'])
    return m

def mat_bark(name):
    # sama seperti sebelumnya
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    n = m.node_tree.nodes
    l = m.node_tree.links
    n.clear()
    out = n.new('ShaderNodeOutputMaterial')
    principled = n.new('ShaderNodeBsdfPrincipled')
    wave = n.new('ShaderNodeTexWave')
    colorramp = n.new('ShaderNodeValToRGB')
    bump = n.new('ShaderNodeBump')
    wave.inputs['Scale'].default_value = 18
    wave.inputs['Distortion'].default_value = 5.5
    colorramp.color_ramp.elements[0].color = (0.33,0.20,0.12,1)
    colorramp.color_ramp.elements[1].color = (0.5,0.33,0.17,1)
    l.new(wave.outputs['Color'], colorramp.inputs['Fac'])
    l.new(colorramp.outputs['Color'], principled.inputs['Base Color'])
    l.new(wave.outputs['Color'], bump.inputs['Height'])
    l.new(bump.outputs['Normal'], principled.inputs['Normal'])
    l.new(principled.outputs['BSDF'], out.inputs['Surface'])
    return m

def mat_moss(name):
    # sama seperti sebelumnya
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    n = m.node_tree.nodes
    l = m.node_tree.links
    n.clear()
    out = n.new('ShaderNodeOutputMaterial')
    principled = n.new('ShaderNodeBsdfPrincipled')
    noise = n.new('ShaderNodeTexNoise')
    colorramp = n.new('ShaderNodeValToRGB')
    bump = n.new('ShaderNodeBump')
    noise.inputs['Scale'].default_value = 24.0
    colorramp.color_ramp.elements[0].color = (0.2,0.36,0.13,1)
    colorramp.color_ramp.elements[1].color = (0.68,0.89,0.52,1)
    l.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
    l.new(colorramp.outputs['Color'], principled.inputs['Base Color'])
    l.new(noise.outputs['Fac'], bump.inputs['Height'])
    l.new(bump.outputs['Normal'], principled.inputs['Normal'])
    l.new(principled.outputs['BSDF'], out.inputs['Surface'])
    return m

def mat_leaf(name):
    # sama seperti sebelumnya
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    n = m.node_tree.nodes
    l = m.node_tree.links
    n.clear()
    out = n.new('ShaderNodeOutputMaterial')
    principled = n.new('ShaderNodeBsdfPrincipled')
    wave = n.new('ShaderNodeTexWave')
    colorramp = n.new('ShaderNodeValToRGB')
    bump = n.new('ShaderNodeBump')
    wave.inputs['Scale'].default_value = 12
    colorramp.color_ramp.elements[0].color = (0.29,0.39,0.08,1)
    colorramp.color_ramp.elements[1].color = (0.58,0.74,0.19,1)
    l.new(wave.outputs['Color'], colorramp.inputs['Fac'])
    l.new(colorramp.outputs['Color'], principled.inputs['Base Color'])
    l.new(wave.outputs['Color'], bump.inputs['Height'])
    l.new(bump.outputs['Normal'], principled.inputs['Normal'])
    l.new(principled.outputs['BSDF'], out.inputs['Surface'])
    return m

def mat_rock(name):
    # sama seperti sebelumnya
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    n = m.node_tree.nodes
    l = m.node_tree.links
    n.clear()
    out = n.new('ShaderNodeOutputMaterial')
    principled = n.new('ShaderNodeBsdfPrincipled')
    noise = n.new('ShaderNodeTexNoise')
    colorramp = n.new('ShaderNodeValToRGB')
    bump = n.new('ShaderNodeBump')
    noise.inputs['Scale'].default_value = 18
    colorramp.color_ramp.elements[0].color = (0.4,0.4,0.4,1)
    colorramp.color_ramp.elements[1].color = (0.68,0.68,0.70,1)
    l.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
    l.new(colorramp.outputs['Color'], principled.inputs['Base Color'])
    l.new(noise.outputs['Fac'], bump.inputs['Height'])
    l.new(bump.outputs['Normal'], principled.inputs['Normal'])
    l.new(principled.outputs['BSDF'], out.inputs['Surface'])
    return m

def mat_root(name):
    # sama seperti sebelumnya
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    n = m.node_tree.nodes
    l = m.node_tree.links
    n.clear()
    out = n.new('ShaderNodeOutputMaterial')
    principled = n.new('ShaderNodeBsdfPrincipled')
    magic = n.new('ShaderNodeTexMagic')
    colorramp = n.new('ShaderNodeValToRGB')
    bump = n.new('ShaderNodeBump')
    magic.inputs['Scale'].default_value = 22
    colorramp.color_ramp.elements[0].color = (0.27,0.14,0.04,1)
    colorramp.color_ramp.elements[1].color = (0.48,0.36,0.23,1)
    l.new(magic.outputs['Color'], colorramp.inputs['Fac'])
    l.new(colorramp.outputs['Color'], principled.inputs['Base Color'])
    l.new(magic.outputs['Color'], bump.inputs['Height'])
    l.new(bump.outputs['Normal'], principled.inputs['Normal'])
    l.new(principled.outputs['BSDF'], out.inputs['Surface'])
    return m

def mat_puddle(name):
    # sama seperti sebelumnya
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    n = m.node_tree.nodes
    l = m.node_tree.links
    n.clear()
    out = n.new('ShaderNodeOutputMaterial')
    principled = n.new('ShaderNodeBsdfPrincipled')
    checker = n.new('ShaderNodeTexChecker')
    colorramp = n.new('ShaderNodeValToRGB')
    bump = n.new('ShaderNodeBump')
    checker.inputs['Scale'].default_value = 10.0
    colorramp.color_ramp.elements[0].color = (0.2,0.2,0.25,1)
    colorramp.color_ramp.elements[1].color = (0.3,0.3,0.5,1)
    l.new(checker.outputs['Color'], colorramp.inputs['Fac'])
    l.new(colorramp.outputs['Color'], principled.inputs['Base Color'])
    l.new(checker.outputs['Fac'], bump.inputs['Height'])
    l.new(bump.outputs['Normal'], principled.inputs['Normal'])
    l.new(principled.outputs['BSDF'], out.inputs['Surface'])
    return m

positions = []
r = 5
for i in range(8):
    angle = i * math.pi * 2 / 8
    positions.append((math.cos(angle) * r, math.sin(angle) * r, 0))
bpy.ops.mesh.primitive_plane_add(size=15, location=(0,0,-0.5)) # alas

objs = []
bpy.ops.mesh.primitive_cone_add(location=positions[0]); objs.append(bpy.context.active_object)          # Soil
bpy.ops.mesh.primitive_uv_sphere_add(location=positions[1]); objs.append(bpy.context.active_object)     # Stone
bpy.ops.mesh.primitive_cylinder_add(location=positions[2]); objs.append(bpy.context.active_object)      # Bark
bpy.ops.mesh.primitive_monkey_add(location=positions[3]); objs.append(bpy.context.active_object)        # Moss
bpy.ops.mesh.primitive_grid_add(location=positions[4]); objs.append(bpy.context.active_object)          # Leaf
bpy.ops.mesh.primitive_uv_sphere_add(location=positions[5]); objs.append(bpy.context.active_object)     # Rock
bpy.ops.mesh.primitive_cylinder_add(location=positions[6]); objs.append(bpy.context.active_object)      # Root
bpy.ops.mesh.primitive_grid_add(location=positions[7]); objs.append(bpy.context.active_object)          # Puddle

materials = [
    mat_ground_soil("Soil"),
    mat_stone("Stone"),
    mat_bark("Bark"),
    mat_moss("Moss"),
    mat_leaf("Leaf"),
    mat_rock("Rock"),
    mat_root("Root"),
    mat_puddle("Puddle")
]
for o, m in zip(objs, materials):
    o.data.materials.append(m)

print("Natural forest floor scene created with revised object types (tugas2_procedural_scene.py)")
