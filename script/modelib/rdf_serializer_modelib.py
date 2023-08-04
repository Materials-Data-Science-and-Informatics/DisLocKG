from rdflib import Graph, Literal
from rdflib.namespace import  Namespace, RDF, XSD
import numpy as np


#crystal structure ontology
CSO = Namespace("https://purls.helmholtz-metadaten.de/disos/cso#")
#dislocation ontology
DISO = Namespace("https://purls.helmholtz-metadaten.de/disos/diso#")
#crystalline-defect-ontology
CDO = Namespace("https://purls.helmholtz-metadaten.de/disos/cdo#")
MDO = Namespace("https://w3id.org/mdo/structure/")
QUDT = Namespace("http://qudt.org/schema/qudt/")
QUDT_UNIT = Namespace("http://qudt.org/vocab/unit/")
QUDT_QK = Namespace("http://qudt.org/vocab/quantitykind/")
MDO_CORE = Namespace("https://w3id.org/mdo/core/")


# function to serializing the cif into resource description framework(RDF) using the crystallography ontology
# returning graph object of rdflib
def cube_edge_length(gmsh_file, burgers_vector):
    with open(gmsh_file, 'r') as file:
    # Read all lines from the file
        lines = file.readlines()

    # Extract the desired information from rows 15 to 22
    start_row = 15
    end_row = 22
    data_list = []

    for line in lines[start_row-1:end_row]:
        # Split the line by spaces
        line_data = line.split()
        # Extract the required values
        values = [float(value) for value in line_data[1:]]
        data_list.append(values)
    
    min_x, min_y, min_z = np.min(data_list, axis=0)
    max_x, max_y, max_z = np.max(data_list, axis=0)

    box = np.array([(min_x, min_y, min_z), (max_x, min_y, min_z), (max_x, max_y, min_z), (min_x, max_y, min_z),
                     (min_x, min_y, max_z), (max_x, min_y, max_z), (max_x, max_y, max_z), (min_x, max_y, max_z)]).tolist()
    
    return  np.linalg.norm(np.array(box[0])-np.array(box[4])) * burgers_vector

    

def _normalized_vector(vector):
    highest = max(map(abs, vector))

    # Divide each component by the highest absolute value if it's not zero
    new_vector = []
    for i in range(len(vector)):
        if highest != 0:
            temp = int(vector[i] / highest)
            new_vector.append(temp)
        else:
            temp = int(vector[i])
            new_vector.append(temp)
    return new_vector

def crystal_rdf_serializer(cif_data, space_group_data, mat_info, ns):
    g = Graph()
    g.parse("https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/Dislocation-Ontology-Suite/main/CSO/crystal-structure-ontology.owl", format="xml")
    g.parse("https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/Dislocation-Ontology-Suite/main/DISO/dislocation-ontology.owl", format="xml")
    # g.parse("../../crystallographic-defect-ontology/crystallographic-defect-ontology.owl", format="xml")

    g.bind("disoKG", ns)
    g.bind("cdo", CDO)
    g.bind("diso", DISO)
    g.bind("cso", CSO)
    g.bind("mdo_structure", MDO)
    g.bind("mdo_core", MDO_CORE)
    g.bind("qudt", QUDT)
    g.bind("unit", QUDT_UNIT)
    g.bind("quantityKind", QUDT_QK)

    # unit_of_length = 2.489e-10 # Burgers vector
    unit_of_length =  mat_info.attrs['b_SI']# Burgers vector

    space_group_data = space_group_data['spacegroup'] # space group data
    
    # crystal structure data
    crystal = ns['crystal']
    Bravais_lattice = ns['Bravais_lattice']
    crystal_structure = ns['crystal_structure']
    crystal_system = ns['crystal_system']
    unit_cell = ns['unit_cell']
    lattice_param_length = ns['lattice_parameter_length']
    lattice_param_angle = ns['lattice_parameter_angle']
    basis = ns['coordinate_basis']
    crystal_coordinate_first_axis = ns['crystal_coordinate_first_axis']
    crystal_coordinate_second_axis = ns['crystal_coordinate_second_axis']
    crystal_coordinate_third_axis = ns['crystal_coordinate_third_axis']
    space_group = ns['space_group']
    point_group = ns['point_group']
    
    
    ## length data value
    length_a = Literal(cif_data['_cell_length_a']*1e-10, datatype=XSD.double) 
    length_b = Literal(cif_data['_cell_length_b']*1e-10, datatype=XSD.double)
    length_c = Literal(cif_data['_cell_length_c']*1e-10, datatype=XSD.double)
    
    ##angle data value
    angle_alpha = Literal(cif_data['_cell_angle_alpha'], datatype=XSD.double)  
    angle_beta =  Literal(cif_data['_cell_angle_beta'], datatype=XSD.double)
    angle_gamma = Literal(cif_data['_cell_angle_gamma'], datatype=XSD.double)


    # Crystal structure initial g
    g.add((crystal, RDF.type, CDO.CrystallineMaterial))
    g.add((crystal, CDO.hasCrystalStructure, crystal_structure))
    g.add((crystal_structure, RDF.type, CSO.CrystalStructure))
    g.add((crystal_structure, CSO.hasLattice, Bravais_lattice))
    g.add((crystal_structure, MDO.hasSpaceGroup, space_group))
    g.add((space_group, RDF.type, MDO.SpaceGroup))
    g.add((space_group, MDO.SpaceGroupID, Literal(space_group_data['number'], datatype=XSD.integer)))
    g.add((space_group, MDO.SpaceGroupSymbol, Literal(space_group_data['symbol'], datatype=XSD.string)))
    g.add((space_group, MDO.hasPointGroup, point_group))
    g.add((point_group, RDF.type, MDO.PointGroup))
    g.add((point_group, MDO.PointGroupHMName, Literal(space_group_data['point_group'], datatype=XSD.string)))
    g.add((Bravais_lattice, RDF.type, CSO.BravaisLattice))
    g.add((Bravais_lattice, CSO.centering, Literal(space_group_data['symbol'][0], datatype=XSD.string)))
    g.add((Bravais_lattice, CSO.hasCrystalSystem, crystal_system))
    g.add((crystal_system, RDF.type, CSO[space_group_data['crystal_system'].capitalize()]))
    g.add((point_group, CSO.isPointGroupOf, crystal_system))
    g.add((Bravais_lattice, CSO.hasUnitCell, unit_cell))
    g.add((unit_cell, RDF.type, CSO.UnitCell))
    g.add((unit_cell, CSO.hasLatticeParameterLength, lattice_param_length))
    g.add((unit_cell, CSO.hasLatticeParameterAngle, lattice_param_angle))
    g.add((lattice_param_length, RDF.type, CSO.LatticeParameterLength))
    g.add((lattice_param_angle, RDF.type, CSO.LatticeParameterAngle))
    g.add((lattice_param_length, CSO.latticeParameterLengthA , length_a))
    g.add((lattice_param_length, CSO.latticeParameterLengthB, length_b))
    g.add((lattice_param_length, CSO.latticeParameterLengthC, length_c))
    g.add((lattice_param_angle, CSO.latticeParameterAngleAlpha, angle_alpha))
    g.add((lattice_param_angle, CSO.latticeParameterAngleBeta, angle_beta))
    g.add((lattice_param_angle, CSO.latticeParameterAngleGamma, angle_gamma))

    # basis of vector
    g.add((basis, RDF.type, MDO.Basis))
    g.add((basis, CSO.hasFirstAxisVector, crystal_coordinate_first_axis))
    g.add((crystal_coordinate_first_axis, RDF.type, MDO.CoordinateVector))
    g.add((crystal_coordinate_first_axis, MDO.X_axisCoordinate, Literal(0.0, datatype=XSD.double)))
    g.add((crystal_coordinate_first_axis, MDO.Y_axisCoordinate, Literal(0.707, datatype=XSD.double)))
    g.add((crystal_coordinate_first_axis, MDO.Z_axisCoordinate, Literal(0.707, datatype=XSD.double)))
    g.add((basis, CSO.hasSecondAxisVector, crystal_coordinate_second_axis))
    g.add((crystal_coordinate_second_axis, RDF.type, MDO.CoordinateVector))
    g.add((crystal_coordinate_second_axis, MDO.X_axisCoordinate, Literal(0.707, datatype=XSD.double)))
    g.add((crystal_coordinate_second_axis, MDO.Y_axisCoordinate, Literal(0.0, datatype=XSD.double)))
    g.add((crystal_coordinate_second_axis, MDO.Z_axisCoordinate, Literal(0.707, datatype=XSD.double)))
    g.add((basis, CSO.hasThirdAxisVector, crystal_coordinate_third_axis))
    g.add((crystal_coordinate_third_axis, RDF.type, MDO.CoordinateVector))
    g.add((crystal_coordinate_third_axis, MDO.X_axisCoordinate, Literal(0.707, datatype=XSD.double)))
    g.add((crystal_coordinate_third_axis, MDO.Y_axisCoordinate, Literal(0.707, datatype=XSD.double)))
    g.add((crystal_coordinate_third_axis, MDO.Z_axisCoordinate, Literal(0.0, datatype=XSD.double)))
    
    return g

def dislocation_structure_serializer(mat_info, cif_data, init_micro, node_data, linker_data, loop_data, ns, key, edge, is_relaxed):
    g = Graph()
    basis = ns['coordinate_basis']
    crystal_structure = ns['crystal_structure']
    crystal = ns['crystal']
    ddd_sim = ns['ddd_sim']
    dislocation_structure = ns['dislocation_structure_{}'.format(key)]
    cube_shape = ns['cube_shape']
    cube_edge_length = ns['cube_edge_length']
    cube_edge_length_qv = ns['cube_edge_length_qv']
    composition = ns['composition']
    g.add((composition, RDF.type, MDO.Composition))
    g.add((cube_shape, RDF.type, DISO.Cube))
    g.add((cube_edge_length, RDF.type, DISO.Length))
    g.add((cube_edge_length_qv, RDF.type, QUDT.QuantityValue))
    g.add((cube_shape, DISO.hasLength, cube_edge_length))
    g.add((cube_edge_length, QUDT.quantityValue, cube_edge_length_qv))
    g.add((cube_edge_length, QUDT.hasQuantityKind, QUDT_QK.Length))
    g.add((cube_edge_length_qv, QUDT.unit, QUDT_UNIT['NanoM']))
    g.add((cube_edge_length_qv, QUDT.numericalValue, Literal(edge, datatype=XSD.double)))

    if key=='input':
        init_density = init_micro.attrs['targetPrismaticLoopDensity']
        init_dislocation_density = ns['initial_dislocation_density']
        init_dislocation_density_qv = ns['initial_dislocation_density_qv']
        g.add((init_dislocation_density, RDF.type, DISO.DislocationDensity))
        g.add((init_dislocation_density_qv, RDF.type, QUDT.QuantityValue))
        g.add((init_dislocation_density, QUDT.quantityValue, init_dislocation_density_qv))
        g.add((init_dislocation_density_qv, QUDT.numericalValue, Literal(init_density, datatype=XSD.double)))
        g.add((init_dislocation_density_qv, QUDT.unit, QUDT_UNIT['PER-M2']))
        g.add((init_dislocation_density, MDO_CORE.relatesToStructure, dislocation_structure))

    unit_of_length =  mat_info.attrs['b_SI']# Burgers vector

    # dislocation microstructure 
    g.add((dislocation_structure, RDF.type, DISO.DislocationStructure))
    if key=='input': 
        g.add((ddd_sim, DISO.hasInputDislocationStructure, dislocation_structure))
        g.add((dislocation_structure, DISO.isRelaxed, Literal(is_relaxed,  datatype=XSD.boolean)))
        g.add((dislocation_structure, DISO.hasShape, cube_shape))
        g.add((dislocation_structure, MDO.hasComposition, composition))
        g.add((composition, MDO.DescriptiveFormula, Literal(cif_data['_chemical_formula_structural'], datatype=XSD.string)))
    elif key=='output': 
        g.add((ddd_sim, DISO.hasOutputDislocationStructure, dislocation_structure))
        g.add((dislocation_structure, DISO.isRelaxed, Literal(is_relaxed,  datatype=XSD.boolean)))
        g.add((dislocation_structure, DISO.hasShape, cube_shape))

    # dimensionless unit
    qv_unitless = ns['quantity_value_unitless']
    g.add((qv_unitless, RDF.type, QUDT.QuantityValue))
    g.add((qv_unitless, QUDT.unit, QUDT_UNIT['UNITLESS']))

    # unit of length
    qv_m = ns['quantity_value_M']
    g.add((qv_m, RDF.type, QUDT.QuantityValue))
    g.add((qv_m, QUDT.unit, QUDT_UNIT['M']))

    # dislocation node data
    for node in node_data:
        id = node['master_id']
        coordinate = node['coordinates']
        # n_v = node['velocity']
        node_individual = ns['node_{}_{}'.format(id, key)]
        node_position_vector = ns['node_{}_position_vector_{}'.format(id, key)]
        node_coordinate = ns['node_{}_coordinate_{}'.format(id, key)]
        # node_velocity = ns['node_{}_velocity'.format(id)]
        # node_vector_velocity_components = ns['node_{}_vector_velocity_components'.format(id)]

        g.add((node_individual, RDF.type, DISO.Node))
        g.add((node_individual, CSO.hasPositionVector, node_position_vector))
        g.add((node_position_vector, RDF.type, CSO.PositionVector))
        g.add((node_position_vector, CSO.hasVectorComponent, node_coordinate))
        g.add((node_coordinate, RDF.type, CSO.VectorComponentOfBasis))
        g.add((node_coordinate, QUDT.quantityValue, qv_m))
        g.add((node_coordinate, QUDT.hasQuantityKind, QUDT_QK.Length))
        g.add((node_coordinate, CSO.firstAxisComponent, Literal(coordinate[0], datatype=XSD.double)))
        g.add((node_coordinate, CSO.secondAxisComponent, Literal(coordinate[1], datatype=XSD.double)))
        g.add((node_coordinate, CSO.thirdAxisComponent, Literal(coordinate[2], datatype=XSD.double)))
        g.add((node_coordinate, CSO.hasBasis, basis))

        # g.add((node_individual, DISO.hasNodeVelocity, node_velocity))
        # g.add((node_velocity, RDF.type, DISO.NodeVelocity))
        # g.add((node_velocity, CSO.hasVectorComponent, node_vector_velocity_components))
        # g.add((node_vector_velocity_components, RDF.type, CSO.VectorComponentOfBasis))
        # g.add((node_vector_velocity_components, QUDT.unit, QUDT_UNIT['M-PER-SEC']))
        # g.add((node_vector_velocity_components, QUDT.quantityKind, QUDT_QK.Velocity))
        # g.add((node_vector_velocity_components, CSO.firstAxisComponent, Literal(n_v[0], datatype=XSD.double)))
        # g.add((node_vector_velocity_components, CSO.secondAxisComponent, Literal(n_v[1], datatype=XSD.double)))
        # g.add((node_vector_velocity_components, CSO.thirdAxisComponent, Literal(n_v[2], datatype=XSD.double)))
        # g.add((node_vector_velocity_components, CSO.hasBasis, basis))
        
    slip_system_list = []
    counter_slip_system = 0 
    
    
    # dislocation loop data
    for loop in loop_data:
        id = loop['id']
        slip_direction_loop = loop['burgers_vector']
        plane_normal = loop['plane_normal']
        plane_origin = loop['plane_origin']
        slip_area = loop['slip_area']

        dislocation_loop = ns['dislocation_{}_{}'.format(id, key)]
        Burgers_vector = ns['dislocation_{}_Burgers_vector_{}'.format(id, key)]
        vector_components_Burgers_vector = ns['dislocation_{}_vector_components_Burgers_vector_{}'.format(id, key)]
        slip_plane = ns['dislocation_{}_slip_plane_{}'.format(id, key)]
        slip_direction = ns['dislocation_{}_slip_direction_{}'.format(id, key)]
        vector_components_slip_direction = ns['dislocation_{}_vector_components_slip_direction_{}'.format(id, key)]
        slip_plane_normal = ns['dislocation_{}_slip_plane_normal_{}'.format(id, key)]
        vector_components_of_slip_plane_normal = ns['dislocation_{}_vector_components_of_slip_plane_normal_{}'.format(id, key)]
        slip_plane_origin = ns['dislocation_{}_slip_plane_origin_{}'.format(id,key)]
        vector_components_slip_plane_origin = ns['dislocation_{}_vector_components_origin_{}'.format(id, key)]
        line = ns['line_{}_{}'.format(id, key)]
        discretized_line = ns['dislocation_{}_discretized_line_{}'.format(id, key)]
        slip_direction_loop_normalized = _normalized_vector(slip_direction_loop)
        plane_normal_normalized = _normalized_vector(plane_normal)

        g.add((dislocation_structure, CDO.hasCrystallographicDefect, dislocation_loop))
        g.add((dislocation_structure, DISO.relatesToCrystallineMaterial, crystal))
        g.add((dislocation_loop, RDF.type, DISO.Dislocation))
        g.add((dislocation_loop, DISO.hasBurgersVector, Burgers_vector))
        g.add((dislocation_loop, DISO.movesOn, slip_plane))
        g.add((crystal_structure, DISO.hasSlipPlane, slip_plane))
        g.add((slip_plane, RDF.type, DISO.SlipPlane))
        g.add((slip_plane, DISO.hasSlipPlaneNormal, slip_plane_normal))
        plane_miller_indice = '({} {} {})'.format(plane_normal_normalized[0], plane_normal_normalized[1], plane_normal_normalized[2])
        # family_plane_miller_indice = '{111}' # for cubic crystal system
        g.add((slip_plane, DISO.planeMillerIndice, Literal(plane_miller_indice, datatype=XSD.string)))
        # g.add((slip_plane, DISO.familyPlaneMillerIndice, Literal(family_plane_miller_indice, datatype=XSD.string)))
        g.add((slip_plane, DISO.hasSlipDirection, slip_direction))
        g.add((slip_direction, RDF.type, DISO.SlipDirection))
        g.add((slip_direction, CSO.hasVectorComponent, vector_components_slip_direction))
        direction_miller_indice = '[{} {} {}]'.format(slip_direction_loop_normalized[0], slip_direction_loop_normalized[1], slip_direction_loop_normalized[2])
        # family_slip_direction_miller_indice = '<110>' # for cubic crystal system
        g.add((slip_direction, DISO.directionMillerIndice, Literal(direction_miller_indice, datatype=XSD.string)))
        # g.add((slip_direction, DISO.familyDirectionMillerIndice, Literal(family_slip_direction_miller_indice, datatype=XSD.string)))
        g.add((vector_components_slip_direction, QUDT.quantityValue, qv_unitless))
        g.add((vector_components_slip_direction, QUDT.hasQuantityKind, QUDT_QK.Dimensionless))
        slip_direction_magnitude = np.linalg.norm(np.asanyarray(slip_direction_loop))
        g.add((slip_direction, CSO.vectorMagnitude, Literal(slip_direction_magnitude, datatype=XSD.double)))
        g.add((vector_components_slip_direction, RDF.type, CSO.VectorComponentOfBasis))
        g.add((vector_components_slip_direction, CSO.firstAxisComponent, Literal(slip_direction_loop[0], datatype=XSD.double)))
        g.add((vector_components_slip_direction, CSO.secondAxisComponent, Literal(slip_direction_loop[1], datatype=XSD.double)))
        g.add((vector_components_slip_direction, CSO.thirdAxisComponent, Literal(slip_direction_loop[2], datatype=XSD.double)))
        g.add((vector_components_slip_direction, CSO.hasBasis, basis))
        g.add((slip_plane_normal, RDF.type, DISO.SlipPlaneNormal))
        slip_plane_direction_miller_indice = '[{} {} {}]'.format(plane_normal_normalized[0], plane_normal_normalized[1], plane_normal_normalized[2])
        g.add((slip_plane_normal, DISO.directionMillerIndice, Literal(slip_plane_direction_miller_indice, datatype=XSD.string)))
        g.add((slip_plane_normal, CSO.hasVectorComponent, vector_components_of_slip_plane_normal))
        g.add((vector_components_of_slip_plane_normal, QUDT.quantityValue, qv_unitless))
        g.add((vector_components_of_slip_plane_normal, QUDT.hasQuantityKind, QUDT_QK.Dimensionless))
        g.add((vector_components_of_slip_plane_normal, RDF.type, CSO.VectorComponentOfBasis))
        g.add((vector_components_of_slip_plane_normal, CSO.firstAxisComponent, Literal(plane_normal[0], datatype=XSD.double)))
        g.add((vector_components_of_slip_plane_normal, CSO.secondAxisComponent, Literal(plane_normal[1], datatype=XSD.double)))
        g.add((vector_components_of_slip_plane_normal, CSO.thirdAxisComponent, Literal(plane_normal[2], datatype=XSD.double)))
        g.add((vector_components_of_slip_plane_normal, CSO.hasBasis, basis))
        g.add((slip_plane, DISO.hasVectorOrigin, slip_plane_origin))
        g.add((slip_plane_origin, RDF.type, DISO.VectorOrigin))
        g.add((slip_plane_origin, CSO.hasVectorComponent, vector_components_slip_plane_origin))
        g.add((vector_components_slip_plane_origin, RDF.type, CSO.VectorComponentOfBasis))
        g.add((vector_components_slip_plane_origin, CSO.firstAxisComponent, Literal(plane_origin[0], datatype=XSD.double)))
        g.add((vector_components_slip_plane_origin, CSO.secondAxisComponent, Literal(plane_origin[1], datatype=XSD.double)))
        g.add((vector_components_slip_plane_origin, CSO.thirdAxisComponent, Literal(plane_origin[2], datatype=XSD.double)))
        g.add((vector_components_slip_plane_origin, CSO.hasBasis, basis))
        g.add((dislocation_loop, DISO.hasMathematicalRepresentation, line))
        g.add((line, RDF.type, DISO.Line))
        g.add((line, DISO.hasNumericalRepresentation, discretized_line))
        g.add((discretized_line, RDF.type, DISO.DiscretizedLine))
        g.add((discretized_line, DISO.slipArea, Literal(slip_area, datatype=XSD.double)))
        g.add((Burgers_vector, RDF.type, DISO.BurgersVector))
        g.add((Burgers_vector, CSO.hasVectorComponent, vector_components_Burgers_vector))
        g.add((vector_components_Burgers_vector, QUDT.quantityValue, qv_m))
        g.add((vector_components_Burgers_vector, QUDT.hasQuantityKind, QUDT_QK.Length))
        Burgers_vector_magnitude = unit_of_length
        g.add((Burgers_vector, CSO.vectorMagnitude, Literal(Burgers_vector_magnitude, datatype=XSD.double)))
        g.add((vector_components_Burgers_vector, RDF.type, CSO.VectorComponentOfBasis))
        g.add((vector_components_Burgers_vector, CSO.firstAxisComponent, Literal(slip_direction_loop[0] * unit_of_length, datatype=XSD.double)))
        g.add((vector_components_Burgers_vector, CSO.secondAxisComponent, Literal(slip_direction_loop[1]  * unit_of_length, datatype=XSD.double)))
        g.add((vector_components_Burgers_vector, CSO.thirdAxisComponent, Literal(slip_direction_loop[2] * unit_of_length, datatype=XSD.double)))
        g.add((vector_components_Burgers_vector, CSO.hasBasis, basis))

        # slip system data 
        _slip_system = '{}_{}'.format(slip_plane_direction_miller_indice, direction_miller_indice)
        if _slip_system not in slip_system_list:
            active_slip_system = ns['active_slip_system_{}_{}'.format(counter_slip_system, key)]
            g.add((crystal_structure, DISO.hasSlipSystem, active_slip_system))
            g.add((active_slip_system, RDF.type, DISO.SlipSystem))
            g.add((active_slip_system, DISO.hasSlipPlaneNormal, slip_plane_normal))
            g.add((active_slip_system, DISO.hasSlipDirection, slip_direction))
            slip_system_list.append(_slip_system)
            counter_slip_system +=1

    # segment/linker data
    for i, linker in enumerate(linker_data):
        segment = ns['segment_{}_{}'.format(i, key)]
        start_node_id = linker['start_node_id']
        end_node_id = linker['end_node_id']
        dislocation_id = linker['loop_id']
        g.add((segment, RDF.type, DISO.Segment))
        g.add((segment, DISO.hasStartNode, ns['node_{}_{}'.format(start_node_id, key)]))
        g.add((segment, DISO.hasEndNode, ns['node_{}_{}'.format(end_node_id, key)]))
        # g.add((segment, DISO.isSegmentOf, ns['dislocation_{}_discretized_line'.format(dislocation_id)]))
        g.add((ns['dislocation_{}_discretized_line_{}'.format(dislocation_id, key)], DISO.hasSegment, segment))
    
    
    return g