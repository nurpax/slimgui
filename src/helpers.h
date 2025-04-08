#pragma once

static bool is_instance_of(PyObject *obj, const char* name) {
    PyObject *mymodule = PyImport_ImportModule("slimgui");
    if (!mymodule) return false;

    PyObject *myclass = PyObject_GetAttrString(mymodule, name);
    Py_DECREF(mymodule);
    if (!myclass) return false;

    int result = PyObject_IsInstance(obj, myclass);
    Py_DECREF(myclass);
    return result != 0;
}

static bool is_boolref(PyObject *obj)   { return is_instance_of(obj, "BoolRef");}
static bool is_intref(PyObject *obj)    { return is_instance_of(obj, "IntRef"); }
static bool is_floatref(PyObject *obj)  { return is_instance_of(obj, "FloatRef"); }
static bool is_doubleref(PyObject *obj) { return is_instance_of(obj, "DoubleRef"); }
static bool is_strref(PyObject *obj)    { return is_instance_of(obj, "StrRef"); }
static bool is_vec2(PyObject *obj)      { return is_instance_of(obj, "Vec2Ref"); }
static bool is_vec3(PyObject *obj)      { return is_instance_of(obj, "Vec3Ref"); }
static bool is_vec4(PyObject *obj)      { return is_instance_of(obj, "Vec4Ref"); }
static bool is_intvec2(PyObject *obj)   { return is_instance_of(obj, "IntVec2Ref"); }
static bool is_intvec3(PyObject *obj)   { return is_instance_of(obj, "IntVec3Ref"); }
static bool is_intvec4(PyObject *obj)   { return is_instance_of(obj, "IntVec4Ref"); }

class BoolRef : public nb::object     { NB_OBJECT(BoolRef, nb::object, "BoolRef", is_boolref) };
class IntRef : public nb::object      { NB_OBJECT_DEFAULT(IntRef, nb::object, "IntRef", is_intref) };
class FloatRef : public nb::object    { NB_OBJECT_DEFAULT(FloatRef, nb::object, "FloatRef", is_floatref) };
class DoubleRef : public nb::object   { NB_OBJECT_DEFAULT(DoubleRef, nb::object, "DoubleRef", is_doubleref) };
class StrRef : public nb::object      { NB_OBJECT_DEFAULT(StrRef, nb::object, "StrRef", is_strref) };
class Vec2Ref : public nb::object     { NB_OBJECT_DEFAULT(Vec2Ref, nb::object, "Vec2Ref", is_vec2) };
class Vec3Ref : public nb::object     { NB_OBJECT_DEFAULT(Vec3Ref, nb::object, "Vec3Ref", is_vec3) };
class Vec4Ref : public nb::object     { NB_OBJECT_DEFAULT(Vec4Ref, nb::object, "Vec4Ref", is_vec4) };
class IntVec2Ref : public nb::object  { NB_OBJECT_DEFAULT(IntVec2Ref, nb::object, "IntVec2Ref", is_intvec2) };
class IntVec3Ref : public nb::object  { NB_OBJECT_DEFAULT(IntVec3Ref, nb::object, "IntVec3Ref", is_intvec3) };
class IntVec4Ref : public nb::object  { NB_OBJECT_DEFAULT(IntVec4Ref, nb::object, "IntVec4Ref", is_intvec4) };

template <typename RefType>
struct RefValueType;

template <> struct RefValueType<BoolRef>     { using type = bool; using storage = std::array<bool, 1>; static constexpr bool copyable = true; };
template <> struct RefValueType<IntRef>      { using type = int; using storage = std::array<int, 1>; static constexpr bool copyable = true; };
template <> struct RefValueType<FloatRef>    { using type = float; using storage = std::array<float, 1>; static constexpr bool copyable = true; };
template <> struct RefValueType<DoubleRef>   { using type = double; using storage = std::array<double, 1>; static constexpr bool copyable = true; };
template <> struct RefValueType<Vec2Ref>     { using type = ImVec2; using storage = std::array<float, 2>; static constexpr bool copyable = true; };
template <> struct RefValueType<Vec3Ref>     { using type = Vec3; using storage = std::array<float, 3>; static constexpr bool copyable = true; };
template <> struct RefValueType<Vec4Ref>     { using type = ImVec4; using storage = std::array<float, 4>; static constexpr bool copyable = true; };
template <> struct RefValueType<IntVec2Ref>  { using type = std::tuple<int, int>; using storage = std::array<int, 2>; static constexpr bool copyable = false; };
template <> struct RefValueType<IntVec3Ref>  { using type = std::tuple<int, int, int>; using storage = std::array<int, 3>; static constexpr bool copyable = false; };
template <> struct RefValueType<IntVec4Ref>  { using type = std::tuple<int, int, int, int>; using storage = std::array<int, 4>; static constexpr bool copyable = false; };

template <typename RefType>
struct RefHelper {
    using ValueType = typename RefValueType<RefType>::type;
    using StorageType = typename RefValueType<RefType>::storage;
    using ElementType = typename StorageType::value_type;
    static constexpr bool copyable = RefValueType<RefType>::copyable;

    RefType obj;
    StorageType data;

    RefHelper(RefType obj_) : obj(obj_) {
        if (!obj.is_none()) {
            ValueType value = nb::cast<ValueType>(nb::getattr(obj, "value"));
            if constexpr (copyable) {
                memcpy(data.data(), &value, sizeof(ValueType));
            } else if constexpr (std::is_same_v<ValueType, std::tuple<int, int>>) {
                auto [a, b] = value;
                data[0] = a;
                data[1] = b;
            } else if constexpr (std::is_same_v<ValueType, std::tuple<int, int, int>>) {
                auto [a, b, c] = value;
                data[0] = a;
                data[1] = b;
                data[2] = c;
            } else if constexpr (std::is_same_v<ValueType, std::tuple<int, int, int, int>>) {
                auto [a, b, c, d] = value;
                data[0] = a;
                data[1] = b;
                data[2] = c;
                data[3] = d;
            } else {
                assert(false && "Unsupported type");
            }
        }
    }

    ~RefHelper() {
        if (!obj.is_none()) {
            ValueType value;
            if constexpr (copyable) {
                memcpy(&value, data.data(), sizeof(ValueType));
            } else if constexpr (std::is_same_v<ValueType, std::tuple<int, int>>) {
                value = std::make_tuple(data[0], data[1]);
            } else if constexpr (std::is_same_v<ValueType, std::tuple<int, int, int>>) {
                value = std::make_tuple(data[0], data[1], data[2]);
            } else if constexpr (std::is_same_v<ValueType, std::tuple<int, int, int, int>>) {
                value = std::make_tuple(data[0], data[1], data[2], data[3]);
            } else {
                assert(false && "Unsupported type");
            }
            nb::setattr(obj, "value", nb::cast(value));
        }
    }

    ElementType* ptr() {
        return !obj.is_none() ? data.data() : nullptr;
    }
};
