// Penmar -> Build Buildings
// Builds the simple buildings in props.csv (type = building): a box with a thin flat roof slab and a door, on the terrain,
// box collider GSPconcrete. Rows of type "prop" (the plane) are only marked with an empty GameObject to drop a model on.
// Copy to Assets/Editor/, props.csv to Assets/Penmar/.
using System.Globalization;
using System.IO;
using UnityEditor;
using UnityEngine;

public static class PenmarProps
{
    [MenuItem("Penmar/Build Buildings")]
    static void Build()
    {
        const string path = "Assets/Penmar/props.csv";
        if (!File.Exists(path)) { EditorUtility.DisplayDialog("Penmar", "No file at " + path, "OK"); return; }
        var old = GameObject.Find("PENMAR_PROPS"); if (old) Object.DestroyImmediate(old);
        var root = new GameObject("PENMAR_PROPS");
        var concrete = Resources.Load<PhysicMaterial>("Physics/GSPconcrete");
        var t = Terrain.activeTerrain;
        var ci = CultureInfo.InvariantCulture;
        foreach (var line in File.ReadAllLines(path))
        {
            var p = line.Split(',');
            if (p.Length < 6 || p[0] == "name") continue;
            float x = float.Parse(p[2], ci), z = float.Parse(p[3], ci), y = float.Parse(p[4], ci), rot = float.Parse(p[5], ci);
            if (t) y = t.SampleHeight(new Vector3(x, 0, z)) + t.transform.position.y;
            var go = new GameObject(p[0]);
            go.transform.parent = root.transform;
            go.transform.position = new Vector3(x, y, z);
            go.transform.rotation = Quaternion.Euler(0, rot, 0);
            if (p[1] != "building") continue;
            float w = float.Parse(p[6], ci), d = float.Parse(p[7], ci), h = float.Parse(p[8], ci);
            Color col; ColorUtility.TryParseHtmlString(p[9], out col);
            var wall = new Material(Shader.Find("Standard")) { color = col }; wall.SetFloat("_Glossiness", 0.1f);
            var roofM = new Material(Shader.Find("Standard")) { color = col * 0.6f }; roofM.SetFloat("_Glossiness", 0.05f);
            var door = new Material(Shader.Find("Standard")) { color = new Color(0.35f, 0.25f, 0.18f) };
            AssetDatabase.CreateAsset(wall, "Assets/Penmar/" + p[0] + "_wall.mat");
            AssetDatabase.CreateAsset(roofM, "Assets/Penmar/" + p[0] + "_roof.mat");
            AssetDatabase.CreateAsset(door, "Assets/Penmar/" + p[0] + "_door.mat");
            Box(go.transform, "Walls", new Vector3(0, h / 2 - 0.2f, 0), new Vector3(w, h + 0.4f, d), wall, concrete);    // 0.2 m sunk into the ground
            Box(go.transform, "Roof", new Vector3(0, h + 0.12f, 0), new Vector3(w + 0.5f, 0.25f, d + 0.5f), roofM, concrete);
            Box(go.transform, "Door_M", new Vector3(-w / 4, 1.05f, -d / 2 - 0.02f), new Vector3(0.9f, 2.1f, 0.05f), door, null);
            Box(go.transform, "Door_W", new Vector3(w / 4, 1.05f, -d / 2 - 0.02f), new Vector3(0.9f, 2.1f, 0.05f), door, null);
        }
        foreach (Transform c in root.GetComponentsInChildren<Transform>())
            GameObjectUtility.SetStaticEditorFlags(c.gameObject, StaticEditorFlags.BatchingStatic);
        UnityEditor.SceneManagement.EditorSceneManager.MarkSceneDirty(root.scene);
    }

    static void Box(Transform parent, string name, Vector3 local, Vector3 size, Material m, PhysicMaterial pm)
    {
        var g = GameObject.CreatePrimitive(PrimitiveType.Cube);
        g.name = name; g.transform.parent = parent;
        g.transform.localPosition = local; g.transform.localRotation = Quaternion.identity; g.transform.localScale = size;
        g.GetComponent<Renderer>().sharedMaterial = m;
        if (pm) g.GetComponent<Collider>().sharedMaterial = pm; else Object.DestroyImmediate(g.GetComponent<Collider>());
    }
}
