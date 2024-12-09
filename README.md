# Fractured Frost: Procedural Ice Destruction

## Project Theme
The theme of this project revolves around the **transformation of natural elements**, focusing on the creation and procedural destruction of ice objects in a virtual environment. By utilizing **Infinigen's procedural generation techniques**, the project crafts intricate and photorealistic ice models and integrates them into **Houdini** for spectacular visual effects that simulate realistic ice destruction. This pipeline combines nature-inspired procedural modeling with cutting-edge simulation techniques, emphasizing themes of **fragility**, **force**, and **transience** in nature.

## Overview
This project develops a pipeline that:
1. Utilizes **Infinigen's algorithm** to procedurally generate custom objects.
2. Integrates these objects into **Houdini** for advanced visual effects.
3. Simulates and renders **realistic ice destruction**, capturing fine details like cracking, shattering, and fracturing dynamics.

## Key Features
- **Procedural Generation**: Using Infinigen’s open-source algorithms to create highly detailed, customizable ice assets.
- **Houdini VFX**: Leveraging Houdini’s node-based simulation tools to design and control ice destruction effects.
- **Pipeline Integration**: Connecting Infinigen-generated assets to Houdini’s workflow for efficiency and scalability.
- **Realism**: Achieving photorealistic results through precise control of materials, lighting, and physics simulations.

## Tools and Technologies
- **Infinigen**: For procedural 3D asset generation.
- **Houdini**: For virtual effects and simulation of ice destruction.
- **Blender/Other 3D Tools**: (Optional) For preprocessing or additional customization.

## Pipeline Steps
1. **Asset Creation**: Generate ice objects using procedural tools, ensuring high fidelity and geometric detail.
2. **Data Export**: Export the generated ice models in compatible formats (e.g., OBJ, FBX) for Houdini.
3. **Import and Setup**: Import ice models into Houdini, applying materials and setting up physical properties (e.g., brittleness, density).
4. **Destruction Simulation**: Use Houdini’s dynamics to simulate ice breaking, shattering, and fragmenting under various forces.


### Results
Examples of rendered outputs showcasing the final ice destruction effects.


### Future Work
Material Diversity: Extend the pipeline to include other natural materials such as glass, stone, or wood, creating a library of destructible objects with unique physical and visual properties.

Language Model Integration: Utilize language models to automate the creation of Python scripts. By interpreting natural language input, users could generate scripts that seamlessly integrate text-based asset creation into the pipeline, from model generation to VFX simulation.



## Milestone 1: Setting Up the PCG System with Basic Object Placement
Study Infinigen's code and develop a PCG system based on it to place objects within a 3D scene.
Tasks:
Read papers to understand the prinnciples and genrated objects. 

Modified and expand the existing code to procedurally generate a greater variety of plants and animals.
Deliverable: A procedurally generated outdoor scene populated with various plants, animals, and objects in randomized, realistic placements.



## Milestone 2: Wrtiing python scripts to create new assets 
Python scripts were developed to procedurally generate new assets based on customizable parameters. These scripts were designed to create variations of existing models by altering attributes such as size, texture, and geometry. Rigorous testing ensured the generated assets were compatible with the rest of the pipeline and met high standards of quality.

Outcome:
![apple]()

![star]()


## Milestone 3: Adding the VFX effects throguh Houdini 
The generated assets were successfully imported into Houdini, where complex destruction simulations were set up. These simulations included scenarios such as ice shattering under force, enhanced by advanced particle systems, lighting, and material shaders. High-quality renders of these effects were produced, showcasing the visual realism and dynamic interactions of the assets.

Outcome:
![vfx]()




## Potential Applications



## Reference 


