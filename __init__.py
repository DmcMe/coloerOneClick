#                        _oo0oo_
#                       o8888888o
#                       88" . "88
#                       (| -_- |)
#                       0\  =  /0
#                     ___/`---'\___
#                   .' \|     |// '.
#                  / \|||  :  |||// \
#                 / _||||| -:- |||||- \
#                |   | \\  -  /// |   |
#                | \_|  ''\---/''  |_/ |
#                \  .-\__  '-'  ___/-. /
#              ___'. .'  /--.--\  `. .'___
#           ."" '<  `.___\_<|>_/___.' >' "".
#          | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#          \  \ `_.   \_ __\ /__ _/   .-` /  /
#      =====`-.____`.___ \_____/___.-`___.-'===== hello bois

bl_info = {
    "name": "Sharder Library",
    "author": "DMC",
    "version": (1, 0),
    "blender": (2, 93, 5),
    "location": "View3D > Toolshelf",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "doc_url": "",
    "category": "Add Shader",
}
import bpy

class ShaderMainPanel(bpy.types.Panel):
    bl_label = "Shader Library"
    bl_idname = "SHADER_PT_MAINPANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Shader Library'

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator('shader.diamond_operator')
        row.operator('shader.emission_operator')
        
        


#create Operator for diamond shader
class Shader_OT_DIAMOND(bpy.types.Operator):      
    bl_label = "Diamond"
    bl_idname = 'shader.diamond_operator'
    
    def execute(self, context):
        #create new shader                          name "Diamond"
        material_diamond = bpy.data.materials.new(name= "testDiamond")
        #Enable use node
        material_diamond.use_nodes = True
        
        material_diamond.node_tree.nodes.remove(material_diamond.node_tree.nodes.get('Principled BSDF'))
        #Create referance to the marterial output
        material_output = material_diamond.node_tree.nodes.get('Material Output')
        #set location node
        material_output.location = (200,0)
        
        glass1_node = material_diamond.node_tree.nodes.new('ShaderNodeBsdfGlass') #adding glass1Node
        glass1_node.location = (-600,0) #set location node
                                            #R G B A
        glass1_node.inputs[0].default_value = (1, 0, 0, 1)
        glass1_node.inputs[2].default_value = 1.446
        
        #glass2
        glass2_node = material_diamond.node_tree.nodes.new('ShaderNodeBsdfGlass') #adding glass1Node
        glass2_node.location = (-600,-150) #set location node
                                            #R G B A
        glass2_node.inputs[0].default_value = (0, 1, 0, 1)
        glass2_node.inputs[2].default_value = 1.0
        
        #glass3
        glass3_node = material_diamond.node_tree.nodes.new('ShaderNodeBsdfGlass') #adding glass1Node
        glass3_node.location = (-600,-300) #set location node
                                            #R G B A
        glass3_node.inputs[0].default_value = (0, 0, 1, 1)
        glass3_node.inputs[2].default_value = 0.8
        
        #glass4
        glass4_node = material_diamond.node_tree.nodes.new('ShaderNodeBsdfGlass') #adding glass1Node
        glass4_node.location = (-600, 150) #set location node
                                            #R G B A
        glass4_node.inputs[0].default_value = (1, 1, 1, 1)
        glass4_node.inputs[2].default_value = 1.1
        
        #adding addShader node1
        add1_node = material_diamond.node_tree.nodes.new('ShaderNodeAddShader')
        #location
        add1_node.location = (-400, -150)
        add1_node.label = "Add 1"
        add1_node.select = False
        
        #adding addShader node2
        add2_node = material_diamond.node_tree.nodes.new('ShaderNodeAddShader')
        #location
        add2_node.location = (-400, 0)
        add2_node.label = "Add 2"
        add2_node.hide = False
        add2_node.select = False
        
        
        add3_node = material_diamond.node_tree.nodes.new('ShaderNodeAddShader')
        add3_node.location = (-100, 0)
        add3_node.label = "Add 3"
        add3_node.hide = False
        add3_node.select = False
        #-----------linkind node------------
        material_diamond.node_tree.links.new(glass1_node.outputs[0],add1_node.inputs[0]) #Glass1 link node Addshader1
        material_diamond.node_tree.links.new(glass2_node.outputs[0],add1_node.inputs[1]) #Glass2 link node Addshader1
        material_diamond.node_tree.links.new(glass3_node.outputs[0], add2_node.inputs[0])
        material_diamond.node_tree.links.new(glass4_node.outputs[0], add2_node.inputs[1])
        #material_diamond.node_tree.links.new(add1_node.outputs[0], mix1_node.inputs[1])
        
        material_diamond.node_tree.links.new(add1_node.outputs[0],add3_node.inputs[0])
        material_diamond.node_tree.links.new(add2_node.outputs[0],add3_node.inputs[1])
        
        material_diamond.node_tree.links.new(add3_node.outputs[0],material_output.inputs[0])
        
        
        bpy.context.object.active_material = material_diamond
        
        return{'FINISHED'}
#-----------------------------------------------------------------------------------------------------------------------------------------------------#
        
        
        #create Operator for diamond shader
class Shader_OT_DIAMOND(bpy.types.Operator): 
    bl_label = "Emission"
    bl_idname = 'shader.emission_operator'
    
    def execute(self, context):
        textpath = os.path.dirname(__file__) + "/texture/11.png"
        bl_label = str(textpath)
        bpy.data.images.load(textpath, check_existing=True)
        mat = bpy.context.view_layer.objects.active.active_material
        tex = bpy.data.images.get('11.png')
        image_node = mat.node_tree.nodes.new('ShaderNodeTexImage')
        image_node.image = tex
        return{'FINISHED'}
#-----------------------------------------------------------------------------------------------------------------------------------------------------#
   
def register():
    bpy.utils.register_class(ShaderMainPanel)
    bpy.utils.register_class(Shader_OT_DIAMOND)
    

def unregister():
    bpy.utils.unregister_class(ShaderMainPanel)
    bpy.utils.unregister_class(Shader_OT_DIAMOND)

if __name__ == "__main__":
    register()
    
