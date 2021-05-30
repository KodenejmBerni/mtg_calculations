#version 330

in vec3 aPos, aCol;
out vec3 vCol;

void main()
{
    gl_Position = vec4(aPos, 1.0);
    vCol = aCol;
}