// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

// Externs
// ------------------------------------
// extern vec3 position;
// extern float size;
// extern vec4 color;
// vec4 transform(vec3 position);


// Varyings
// ------------------------------------
varying vec4  v_color;

// Main
// ------------------------------------
void main()
{
    fetch_uniforms();
    v_color = color;

    gl_Position = $transform(position);
}
