#include <glad/glad.h>
#include <stdio.h>
#include <iostream>
#include <GLFW/glfw3.h>

using namespace std;

// vao objet
//vbo attribut

int main(){
    //intialiser glfw <-> checks if GLFW (the graphics library) initializes properly
    if (!glfwInit()){
        printf("Could not initialize glfw.\n");
        return -1;
    }
    //Creation de la fenetre
    GLFWwindow* window;
    window = glfwCreateWindow(640, 480, "OpenGL TP 1", NULL, NULL);
    if (!window){
        glfwTerminate();
        return -1;
    }

   // l’initialisation de GLFW :
    glfwWindowHint(GLFW_SAMPLES, 4);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR , 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE,GLFW_OPENGL_CORE_PROFILE);


    //This line makes the created GLFW window the current OpenGL rendering context. This is necessary to perform OpenGL rendering within this window
    glfwMakeContextCurrent(window);

    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)){
        cout << "Could not initialize GLAD" << endl;
        return -1;
    }

    //- Déclarer les sommets :
    float vertices[] = {
        1.0f, 0.0f, 0.0f,
        0.0f, 1.0f, 0.0f,
        -1.0f, 0.0f, 0.0f,
    };

    // - Déclarer les buffers :
    GLuint VAO;
    GLuint VBO;

    //- Générer et lier le VAO :
    glGenVertexArrays(1, &VAO);
    // lier le buffer / le rendre actif
    glBindVertexArray(VAO);

    glGenBuffers(1, &VBO);
    glBindBuffer(GL_ARRAY_BUFFER, VBO);


    // - Fournir les sommets à OpenGL pour qu’ils soient placés dans le VBO :
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

    //- Lier le premier buffer d'attributs (les sommets) et configurer le pointeur :
    // temchi m3a cheyder t9olo f la pos 0 3ndk 3 params qui sont des float... yinterpriter les données
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat) , (void*)0 );

    // - On indique à OpenGL qu'on utilise un attribut donné :
    glEnableVertexAttribArray(0);

    // - Débinder le VAO et le VBO :
    glBindBuffer(GL_ARRAY_BUFFER, 0);
    glBindVertexArray(0);

    //Definir la boucle d'affichage. Elle sera appelle a chaque fois que la fenetre sera rafraichie.
    while (!glfwWindowShouldClose(window)){
            glClearColor(0.3f,0.3f,0.5f,1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

       // - Lier le VAO :
        glBindVertexArray(VAO);

           //- Dessiner le triangle :
        glDrawArrays(GL_TRIANGLES, 0, 3);




        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    // - En sortant de la boucle d’affichage, on procède au nettoyage :
    glDeleteVertexArrays(1, &VAO);
    glDeleteBuffers(1, &VBO);


    glfwDestroyWindow(window);
    glfwTerminate();
    return 0;
}
