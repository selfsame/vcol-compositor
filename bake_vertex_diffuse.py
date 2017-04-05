# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK ##### http://s3.selfsamegames.com.s3.amazonaws.com/users/jplur/published/sausage.html

# <pep8 compliant>

bl_info = {
    "name": "Vertex Diffuse Bake",
    "author": "twitter.com/jplur_",
    "version": (1, 0),
    "blender": (2, 56, 0),
    "location": "Render > Clay Render",
    "description": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Render"}

import bpy, bmesh
from bpy.props import BoolProperty
from mathutils import *
from math import *
from bpy_extras.io_utils import axis_conversion
from datetime import datetime

def getGlobalAO(context, vertex, ob, distance, rays):
        pos = ob.matrix_world * vertex.co
        rot = ob.matrix_world.to_3x3()
        normal = rot * vertex.normal
        normal.normalize()
        rays = [r for r in rays if r.dot(normal) > -0.5 ]
        hits = len(rays)
        for ray in rays:
            ray_start_position = pos + (normal * .001)
            ray_end_position = ray_start_position + (ray * distance)
                        
            # Cast the ray
            hit, hit_position, hit_normal, i, o, m = context.scene.ray_cast(ray_start_position, ray_end_position)
                        
            if hit == False:
                hits -= 1
            else:
                difference = ray_start_position - hit_position
                factor = difference.magnitude / distance
                hits -= factor**2
        return hits / len(rays)

def do_ao(context):
    rays =  [Vector((0.10238095372915268, -0.31508979201316833, -0.9435234665870667)), Vector((0.7002239227294922, -0.2680315375328064, -0.6616989374160767)), Vector((-0.2680342197418213, -0.194736510515213, -0.9435228705406189)), Vector((-0.2680342197418213, 0.194736510515213, -0.9435228705406189)), Vector((0.10238095372915268, 0.31508979201316833, -0.9435234665870667)), Vector((0.9049891233444214, -0.2680312693119049, -0.3303844928741455)), Vector((0.024746602401137352, -0.9435214400291443, -0.3303861618041992)), Vector((-0.8896973133087158, -0.31509464979171753, -0.330384761095047)), Vector((-0.5746018886566162, 0.748783528804779, -0.33038756251335144)), Vector((0.5345758199691772, 0.7778645753860474, -0.3303864300251007)), Vector((0.8026090860366821, -0.583126425743103, -0.1256270706653595)), Vector((-0.3065689504146576, -0.9435215592384338, -0.12562866508960724)), Vector((-0.9920774102210999, -0.0, -0.12562832236289978)), Vector((-0.3065689504146576, 0.9435215592384338, -0.12562866508960724)), Vector((0.8026090860366821, 0.583126425743103, -0.12562710046768188)), Vector((0.40894609689712524, -0.628425121307373, 0.6616984605789185)), Vector((-0.47129952907562256, -0.5831223726272583, 0.6616987586021423)), Vector((-0.7002239227294922, 0.2680315375328064, 0.6616989374160767)), Vector((0.03853040188550949, 0.7487789988517761, 0.6616989374160767)), Vector((0.7240421772003174, 0.19473609328269958, 0.6616953611373901)), Vector((-0.0385303869843483, -0.7487789988517761, -0.6616988778114319)), Vector((0.18759427964687347, -0.5773453116416931, -0.7946575880050659)), Vector((0.47129952907562256, -0.5831223726272583, -0.6616987586021423)), Vector((0.7002239227294922, 0.2680315375328064, -0.6616989374160767)), Vector((0.6070604920387268, 0.0, -0.7946555614471436)), Vector((0.33130452036857605, 0.0, -0.9435237646102905)), Vector((-0.7240421772003174, -0.19473609328269958, -0.6616953611373901)), Vector((-0.4911194145679474, -0.35682106018066406, -0.7946574687957764)), Vector((-0.40894615650177, -0.6284251809120178, -0.6616984009742737)), Vector((-0.40894615650177, 0.6284251809120178, -0.6616984009742737)), Vector((-0.4911194145679474, 0.35682106018066406, -0.7946574687957764)), Vector((-0.7240421772003174, 0.19473609328269958, -0.6616953611373901)), Vector((0.47129952907562256, 0.5831223726272583, -0.6616987586021423)), Vector((0.18759427964687347, 0.5773453116416931, -0.7946575880050659)), Vector((-0.0385303869843483, 0.7487789988517761, -0.6616988778114319)), Vector((0.9920774102210999, 0.0, 0.12562832236289978)), Vector((0.9822458028793335, 0.0, -0.18759854137897491)), Vector((0.9049891233444214, 0.2680312693119049, -0.3303844928741455)), Vector((0.3065689504146576, -0.9435215592384338, 0.12562866508960724)), Vector((0.30353087186813354, -0.9341713786125183, -0.1875973641872406)), Vector((0.5345758199691772, -0.7778645753860474, -0.3303864300251007)), Vector((-0.8026090860366821, -0.583126425743103, 0.12562710046768188)), Vector((-0.7946555018424988, -0.5773478746414185, -0.18759500980377197)), Vector((-0.5746018886566162, -0.748783528804779, -0.33038756251335144)), Vector((-0.8026090860366821, 0.583126425743103, 0.1256270706653595)), Vector((-0.7946555018424988, 0.5773478746414185, -0.18759500980377197)), Vector((-0.8896973133087158, 0.31509464979171753, -0.330384761095047)), Vector((0.3065689504146576, 0.9435215592384338, 0.12562866508960724)), Vector((0.30353087186813354, 0.9341713786125183, -0.1875973641872406)), Vector((0.024746602401137352, 0.9435214400291443, -0.3303861618041992)), Vector((0.5746018886566162, -0.748783528804779, 0.33038756251335144)), Vector((0.7946555018424988, -0.5773478746414185, 0.18759498000144958)), Vector((0.8896973133087158, -0.31509464979171753, 0.330384761095047)), Vector((-0.5345758199691772, -0.7778645753860474, 0.3303864300251007)), Vector((-0.30353087186813354, -0.9341713786125183, 0.1875973641872406)), Vector((-0.024746602401137352, -0.9435214400291443, 0.3303861618041992)), Vector((-0.9049891233444214, 0.2680312693119049, 0.3303844928741455)), Vector((-0.9822458028793335, 0.0, 0.18759854137897491)), Vector((-0.9049891233444214, -0.2680312693119049, 0.3303844928741455)), Vector((-0.024746602401137352, 0.9435214400291443, 0.3303861618041992)), Vector((-0.30353087186813354, 0.9341713786125183, 0.1875973641872406)), Vector((-0.5345758199691772, 0.7778645753860474, 0.3303864300251007)), Vector((0.8896973133087158, 0.31509464979171753, 0.330384761095047)), Vector((0.7946555018424988, 0.5773478746414185, 0.18759502470493317)), Vector((0.5746018886566162, 0.748783528804779, 0.33038756251335144)), Vector((0.2680342197418213, -0.19473661482334137, 0.9435228705406189)), Vector((0.4911193251609802, -0.35682108998298645, 0.7946574687957764)), Vector((0.7240421772003174, -0.19473609328269958, 0.6616953611373901)), Vector((-0.10238088667392731, -0.3150898814201355, 0.9435234665870667)), Vector((-0.1875942051410675, -0.5773453712463379, 0.7946576476097107)), Vector((0.03853040188550949, -0.7487789988517761, 0.6616989374160767)), Vector((-0.33130452036857605, 0.0, 0.9435237646102905)), Vector((-0.6070604920387268, 0.0, 0.7946555614471436)), Vector((-0.7002239227294922, -0.2680315375328064, 0.6616989374160767)), Vector((-0.10238088667392731, 0.3150898814201355, 0.9435234665870667)), Vector((-0.1875942051410675, 0.5773453712463379, 0.7946576476097107)), Vector((-0.47129952907562256, 0.5831223726272583, 0.6616987586021423)), Vector((0.2680342197418213, 0.19473661482334137, 0.9435228705406189)), Vector((0.4911193251609802, 0.35682108998298645, 0.7946574687957764)), Vector((0.40894609689712524, 0.628425121307373, 0.6616984605789185))]

    obj = context.active_object
    obj.VBAKE.BAKED = True
    if not "AO" in obj.data.vertex_colors:
        obj.data.vertex_colors.new("AO")
    FALLOFF = 1

    bm = bmesh.new()
    
    STRENGTH = obj.VBAKE.AO_STRENGTH 
    o_mesh = obj.data
    bm.from_mesh(obj.data)
    color = bm.loops.layers.color["AO"]
    for vert in bm.verts:
        for loop in vert.link_loops:
            loop[color] = (1, 1, 1)

    for vert in bm.verts:
        
        result = getGlobalAO(context,vert, obj, obj.VBAKE.AO_STRENGTH , rays)
        result = 1-result
        for loop in vert.link_loops:
                loop[color] = (result, result, result)     
        # concave = .001
        # convex = .001
        # cave_len = 0
        # vex_len = 0
        
        # for edge in vert.link_edges:
        #     l = edge.calc_length()
        #     if edge.is_convex:
        #         convex += 1
        #         vex_len += l
                
        #     else:
        #         concave += 1
        #         cave_len += l
        # if concave > convex:
        #     mod = -1
        #     mag = (cave_len)*cave_len
        # else:    
        #     mod = 1
        #     mag = vex_len*vex_len
        # mag = mag * STRENGTH 

        # if len(vert.link_faces) > 1:
        #     total = 0

        #     a = .6 + mod * (((vert.calc_shell_factor()*vert.calc_shell_factor() ))*mag)

        #     for loop in vert.link_loops:
        #         loop[color] = (a, a, a)

    #bm.to_mesh(obj.data)
    return bm

def do_magic(context, obj=False):
    ms = datetime.now().microsecond
    lights = []
    for o in context.scene.objects:
        if o.type == "LAMP":
            lights.append(o)
    #print(lights)
    if obj is False:
        obj = context.active_object
    obj.VBAKE.BAKED = True
    if not "LIGHT" in obj.data.vertex_colors:
        obj.data.vertex_colors.new("LIGHT")
    bm = bmesh.new()
    obm = bmesh.new() 
    o_mesh = obj.data
    mesh = obj.to_mesh(scene = bpy.context.scene, apply_modifiers = True, settings = 'PREVIEW')
    bm.from_mesh(mesh)
    obm.from_mesh(o_mesh)
    color = bm.loops.layers.color["LIGHT"]
    ocolor = obm.loops.layers.color["LIGHT"]
    obcolor = Vector(obj.color).xyz
    emit = 0
    if len(obj.data.materials) > 0:
        emit = obj.data.materials[0].emit
    find = 0
    for face in bm.faces:
        lind = 0
        for loop in face.loops:
            vcol = loop[color]
            vquat = obj.matrix_world.decompose()[1]
            v = loop.vert 
            n = v.normal * obj.matrix_world.inverted()
            n.normalize()
            co = (v.co * obj.matrix_world) + obj.location #* obj.matrix_world
            final = Vector((0,0,0)) 
            for lamp in lights:
                if lamp.data.type == "SUN":
                    energy = lamp.data.energy
                    lcolor = lamp.data.color
                    lv = lamp.matrix_world.to_quaternion() * Vector((0,0,1))
                    d = lv.dot(n) * energy
                    if d > 0:
                        final = final + ( (Vector((1,1,1)).xyz*d)/2 + (Vector(lcolor)*d)/2 )
                    #final = final + ( Vector((lcolor.r*obcolor[0],lcolor.g*obcolor[1],lcolor.b*obcolor[2]))  * d)
                else:
                    lv = lamp.location - co
                    distance = lv.length 
                    energy = lamp.data.energy*.1
                    lcolor = lamp.data.color

                    intensity = (lamp.data.distance*energy/(lamp.data.distance*energy + distance*distance))

                    d = n.dot(lv)
                    f = d*(intensity)
                    if d > 0:
                        final = final + ( Vector(lcolor) * f)/2 + ( obcolor * f )/2

            lc = Vector((vcol.r,vcol.b,vcol.g))  
            fc = final * lc

            final = (obcolor * emit) + (final * (1-emit))
            obm.faces.ensure_lookup_table()
            obm.faces[find].loops[lind][ocolor] = (final[0], final[1], final[2])
            lind += 1
        find += 1
    return obm

class BakeVertexDiffuse(bpy.types.Operator):
    bl_idname      = 'bake_vertex_diffuse.bake'
    bl_label       = "Add list item"
    bl_description = "Add list item"

    def invoke(self, context, event):
        bm = do_magic(context)
        mix_vcol(context, bm)
        return{'FINISHED'}

class BakeVertexAO(bpy.types.Operator):
    bl_idname      = 'bake_vertex_ao.bake'
    bl_label       = "Add list item"
    bl_description = "Add list item"

    def invoke(self, context, event):
        bm = do_ao(context)
        mix_vcol(context, bm)
        return{'FINISHED'}
    
def mix_vcol(context, bm=False):
    obj = context.active_object
    obcolor = Vector(obj.color).xyz
    
    if not bm:
        bm = bmesh.new()
        bm.from_mesh(obj.data)
    result_layer = bm.loops.layers.color['Col']
    colors = []
    for stack in obj.VBAKE_LAYER:
        if stack.layer in bm.loops.layers.color.keys():
            colors.append( bm.loops.layers.color[stack.layer] )
        else:
            colors.append(False)
    for vert in bm.verts:
        for loop in vert.link_loops:
            sfac = False
            oc = obcolor * obj.VBAKE.MIX_OBCOLOR
            for i, stack in enumerate(obj.VBAKE_LAYER):
                if colors[i] != False:
                    if stack.stack_factor == True:
                        sfac = i
                    else:
                        nc = Vector(loop[colors[i]])
                        if stack.invert == True:
                            nc = Vector((1,1,1)) - nc
                        if sfac != False:
                            f = Vector(loop[colors[sfac]]).normalized().length * stack.factor
                            sfac = False
                        else:
                            f = stack.factor
                        oc = blend(oc,nc, stack.mix, f) 


            loop[result_layer] = (oc.x, oc.y, oc.z)
    bm.to_mesh(obj.data)
    
def blend(v1, v2, type, factor=.5):
    f = factor
    uf = 1 - factor
    if type == "mix":
        return v1*uf + v2*f
    if type == "add":
        return v1*uf + (v1 + v2)*f
    if type == "subtract":
        return v1*uf - (v1 + v2)*f
    if type == "multiply":
        v4 = v1
        return v1*uf + Vector([ v1.x*v2.x, v1.y*v2.y, v1.z*v2.z ])*f
    if type == "darken":
        n = []
        for i in [0,1,2]:
            n.append(min(v1[i], v2[i]))
        return v1*uf + Vector(n)*f
    if type == "lighten":
        n = []
        for i in [0,1,2]:
            n.append(max(v1[i], v2[i]))
        return v1*uf + Vector(n)*f
    if type == "screen":
        n = []
        for i in [0,1,2]:
            n.append(1 - (1 -v1[i])* (1 - v2[i]))
        return v1*uf + Vector(n)*f
    return v2
            
def UPDATE_AO_STRENGTH(self, context):
    obj = context.active_object
    if is_ready(obj):
        do_magic(context)
        do_ao(context)
        mix_vcol(context)
    
def UPDATE_VBAKE_POS(self, context):
    obj = context.active_object
    if is_ready(obj):
        do_magic(context)
        mix_vcol(context)
    
def UPDATE_MIX(self, context):
    obj = context.active_object
    if is_ready(obj):
        mix_vcol(context)
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        
def ACTIVATION(self, context):
    obj = context.active_object
    if obj.VBAKE.BAKED == True:
        if not "Col" in obj.data.vertex_colors:
            obj.data.vertex_colors.new("Col")
        if not "AO" in obj.data.vertex_colors:
            obj.data.vertex_colors.new("AO")
        if not "LIGHT" in obj.data.vertex_colors:
            obj.data.vertex_colors.new("LIGHT")
        
    
def is_ready(obj):
    ms = datetime.now().microsecond

    if abs(obj.VBAKE.LAST_UPDATE - ms) > 2000:
        obj.VBAKE.LAST_UPDATE = ms
        return True
    return False


class VBAKE_group(bpy.types.PropertyGroup):
    BAKED = bpy.props.BoolProperty(update=ACTIVATION)
    AO_STRENGTH = bpy.props.FloatProperty(default = 15.0, min=0, max=1000)
    MIX_OBCOLOR = bpy.props.FloatProperty(default = 1.0, update=UPDATE_MIX, min=0, max=1)
    MIX_AO = bpy.props.FloatProperty(default = .5, update=UPDATE_MIX, min=0, max=1)
    MIX_LIGHT = bpy.props.FloatProperty(default = .5, update=UPDATE_MIX, min=0, max=1)
    LAST_UPDATE = bpy.props.FloatProperty(default = 0)  
    
    AO_TARGET = bpy.props.StringProperty(default = "AO")  
    LIGHT_TARGET = bpy.props.StringProperty(default = "LIGHT")  
    
    CACHE_LOC = bpy.props.FloatVectorProperty()  
    CACHE_SCALE = bpy.props.FloatVectorProperty() 

    AO_MIX_TYPE = bpy.props.EnumProperty(name="AO Blend",
            items=(('mix', "Mix", ""),
                   ('add', "Add", ""),
                   ('subtract', "Subtract", ""),
                   ('multiply', "Multiply", ""),
                   ('lighten', "Lighten", ""),
                   ('darken', "Darken", ""),
                   ('screen', "Screen", ""),
                   ('overlay', "Overlay", ""),
                   ('hardlight', "HardLight", "")
                   ),
            default='mix', update=UPDATE_MIX
            )
    LIGHT_MIX_TYPE = bpy.props.EnumProperty(name="Blend",
            items=(('mix', "Mix", ""),
                   ('add', "Add", ""),
                   ('subtract', "Subtract", ""),
                   ('multiply', "Multiply", ""),
                   ('lighten', "Lighten", ""),
                   ('darken', "Darken", ""),
                   ('screen', "Screen", ""),
                   ('overlay', "Overlay", ""),
                   ('hardlight', "HardLight", "")
                   ),
            default='mix', update=UPDATE_MIX
            )
bpy.utils.register_class(VBAKE_group)
bpy.types.Object.VBAKE = bpy.props.PointerProperty(type=VBAKE_group)


########################
##  UI List for vertex color stack

class VBAKE_LAYER(bpy.types.PropertyGroup):
    stack_factor = bpy.props.BoolProperty(name="stack factor",update=UPDATE_MIX)
    name = bpy.props.StringProperty(name="vertex color name", default="Col")
    invert = bpy.props.BoolProperty(name="invert",update=UPDATE_MIX)
    factor = bpy.props.FloatProperty(default = 1.0, update=UPDATE_MIX, min=0, max=1)
    mix = bpy.props.EnumProperty(name="AO Blend",
            items=(('mix', "Mix", ""),
                   ('add', "Add", ""),
                   ('subtract', "Subtract", ""),
                   ('multiply', "Multiply", ""),
                   ('lighten', "Lighten", ""),
                   ('darken', "Darken", ""),
                   ('screen', "Screen", ""),
                   ('overlay', "Overlay", ""),
                   ('hardlight', "HardLight", "")
                   ), default='mix', update=UPDATE_MIX)

    def refresh(self, context):
        result = []
        obj = context.active_object
        vcols = obj.data.vertex_colors
        for name in vcols.keys():
            result.append( (name, name, '' ))
        return result
        
    def set_enum(self, value):
        pass
    def update_layers(self, context):
        pass
        
    layer = bpy.props.EnumProperty(items=refresh,update=UPDATE_MIX)
 
bpy.utils.register_class(VBAKE_LAYER)
bpy.types.Object.VBAKE_LAYER = bpy.props.CollectionProperty(type=VBAKE_LAYER)
bpy.types.Object.VBAKE_LAYER_index = bpy.props.IntProperty(default=-1)

class VBAKE_STACK_class(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        ob = data
        sclass = item

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.scale_y = 1.25
            row = layout.row() #layout.row().box().row()
            #row.label(text=sclass.name if sclass.name else "", translate=False, icon_value=icon)
            
            row = layout.row().split(.1)
            row.separator()
            row.prop(sclass, "stack_factor", text="", icon='LINKED')

            row = layout.row().split(1)
            row.prop(sclass, "layer", text="", icon='COLOR')
            row = layout.row().split(.3)
            row.prop(sclass, "invert", text="", icon='IMAGE_ALPHA')
            row.prop(sclass, "mix", text="")
            row = layout.row().split(1)
            row.prop(sclass, "factor", text="")

        # 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

bpy.utils.register_class(VBAKE_STACK_class)

class VBAKE_STACK_OT_add(bpy.types.Operator):
        bl_idname      = 'vbake_stack.add'
        bl_label       = "Add list item"
        bl_description = "Add list item"
 
        def invoke(self, context, event):
                obj = context.active_object
                obj.VBAKE_LAYER.add()
                obj.VBAKE_LAYER_index = len(obj.VBAKE_LAYER)-1
                UPDATE_MIX(self,context)
                return{'FINISHED'}
class VBAKE_STACK_OT_add(bpy.types.Operator):
        bl_idname      = 'vbake_color.add'
        bl_label       = "Add list item"
        bl_description = "Add list item"
 
        def invoke(self, context, event):
                obj = context.active_object
                obj.VBAKE_LAYER.add()
                obj.VBAKE_LAYER_index = len(obj.VBAKE_LAYER)-1
                UPDATE_MIX(self,context)
                return{'FINISHED'}
            
class VBAKE_STACK_OT_remove(bpy.types.Operator):

        bl_idname      = 'vbake_stack.remove'
        bl_label       = "Add list item"
        bl_description = "Add list item"
 
        def invoke(self, context, event):

                obj = context.active_object
                obj.VBAKE_LAYER.remove(obj.VBAKE_LAYER_index)
                if obj.VBAKE_LAYER_index > len(obj.VBAKE_LAYER): obj.VBAKE_LAYER_index = len(obj.VBAKE_LAYER)-1
                UPDATE_MIX(self,context)
                return{'FINISHED'}
class VBAKE_STACK_OT_up(bpy.types.Operator):
        bl_idname      = 'vbake_stack.up'
        bl_label       = "move selected pass up"
        bl_description = "move selected pass up"
        def invoke(self, context, event):
                obj = context.active_object
                i = obj.VBAKE_LAYER_index
                t = len(obj.VBAKE_LAYER)-1
                n = i-1
                if n < 0:
                    n = t
                if n > t:
                    n = 0
                obj.VBAKE_LAYER.move(i,n)
                obj.VBAKE_LAYER_index = n
                UPDATE_MIX(self,context)
                return{'FINISHED'}
class VBAKE_STACK_OT_down(bpy.types.Operator):
        bl_idname      = 'vbake_stack.down'
        bl_label       = "move selected pass down"
        bl_description = "move selected pass down"
        def invoke(self, context, event):
                obj = context.active_object
                i = obj.VBAKE_LAYER_index
                t = len(obj.VBAKE_LAYER)-1
                n = i+1
                if n < 0:
                    n = t
                if n > t:
                    n = 0
                obj.VBAKE_LAYER.move(i,n)
                obj.VBAKE_LAYER_index = n
                UPDATE_MIX(self,context)
                return{'FINISHED'}


class RENDER_PT_hello(bpy.types.Panel ):
    
    @classmethod
    def poll(cls, context):
        scene = context.scene
        obj = context.active_object
        return bpy.context.mode in ['PAINT_VERTEX','OBJECT'] and obj.type == "MESH"

    bl_label = "Vertex Bake"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        obj = context.active_object
        self.layout.prop(obj.VBAKE, "BAKED", text="")


    def draw(self, context):
        obj = context.active_object
        layout = self.layout
        layout.active = obj.VBAKE.BAKED
        scene = context.scene
        
        row = layout.row()
        col = row.column()
        box = col.box()
        if obj.VBAKE.LIGHT_TARGET not in obj.data.vertex_colors.keys():
            box.operator('bake_vertex_diffuse.bake', text="Bake Lighting", icon='CHECKBOX_DEHLT')
        else:
            box.operator('bake_vertex_diffuse.bake', text="Re-Bake Lighting", icon='CHECKBOX_HLT')
        row2 = box.row()
        row2.label("target")
        row2.prop(obj.VBAKE, "LIGHT_TARGET", text="")
        
        col = row.column()
        box = col.box()
        if obj.VBAKE.AO_TARGET not in obj.data.vertex_colors.keys():
            box.operator('bake_vertex_ao.bake', text="Bake AO", icon='CHECKBOX_DEHLT')
        else:
            box.operator('bake_vertex_ao.bake', text="Re-Bake AO", icon='CHECKBOX_HLT')
        row = box.row()
        row.label("target")
        row.prop(obj.VBAKE, "AO_TARGET", text="")
        row = box.row()
        row.label("distance")
        row.prop(obj.VBAKE, "AO_STRENGTH", text="")
        row = layout.row()
        row.label("obColor")
        row.label("mix factor")
        row = layout.row()
        col = row.column()
        rr = col.row()
        rr.prop(context.active_object, "color", text="" )
        col = row.column()
        rrr = col.row()
        rrr.prop(obj.VBAKE, "MIX_OBCOLOR", text="")
        row = layout.row()
        sp = row.split(1)
        sp.template_list("VBAKE_STACK_class", "VBAKE_STACK_class_list", obj, 'VBAKE_LAYER', obj, 'VBAKE_LAYER_index', rows=3)
        spr = row.split(1)
        col = spr.column()
        
        if len(obj.VBAKE_LAYER) > 0 and obj.VBAKE_LAYER_index >= 0:
            
            col.operator("vbake_stack.up", text="", icon='TRIA_UP')
            col.operator("vbake_stack.down", text="", icon='TRIA_DOWN')
            col.operator('vbake_stack.remove', text="", icon="ZOOMOUT")
        row = layout.row()
        row.operator('vbake_stack.add', text="add layer pass", icon="ZOOMIN")
        row.operator('vbake_color.add', text="add color pass", icon="COLOR")
        
def state_changed(scene):
    for obj in bpy.context.scene.objects:
        if obj.is_updated and not obj.is_updated_data:
            if obj.VBAKE.BAKED is True:
                if is_ready(obj):

                    dv = Vector(obj.VBAKE.CACHE_LOC) - obj.location
                    if dv.length > 1:
                        obj.VBAKE.CACHE_LOC[0] = obj.location.x
                        obj.VBAKE.CACHE_LOC[1] = obj.location.y
                        obj.VBAKE.CACHE_LOC[2] = obj.location.z
                        print("UPDATE "+obj.name)
                        bpy.ops.bake_vertex_diffuse.bake("INVOKE_DEFAULT")
                    
if len(bpy.app.handlers.scene_update_post) > 0:
    bpy.app.handlers.scene_update_post.pop()
bpy.app.handlers.scene_update_post.append(state_changed)

def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()