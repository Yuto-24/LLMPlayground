# RELEASE NOTE

Version 1.4.0 (2024-12-19)

You can see detail [here (GitLab)](http://macdok01.tdc8f.otsuka-shokai.co.jp:9010/mac_aitec/compare_llm_streamlit/-/releases).

## What's new

- Add cotomi v2

## Available Models

| Pages             | Base model                                                                            | Training    | Release     | Remarks                                                                                                                                                                                     |
| ----------------- | ------------------------------------------------------------------------------------- | ----------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Qwen2 72B DOMAIN  | [Qwen2-72B-GPTQ-INT4](https://huggingface.co/Qwen/Qwen2-72B-Instruct-GPTQ-Int4)       | Domain Data | iitgpu05    | Current best domain-model. Permanently deployed until next best model appear.<br>**現在の最良のドメイン (大塚商会の知識を学習した)** モデル。次の最良モデルが現れるまで永久に展開されます。 |
| Qwen2.5 72B       | [Qwen2.5-72B-GPTQ-INT4](https://huggingface.co/Qwen/Qwen2.5-72B-Instruct-GPTQ-Int4)   | None        | iitgpu01    | Release permanently.<br>永久にリリースされます。                                                                                                                                            |
| cotomi pro        | cotomi-Pro                                                                            | None        | On-premises | **Made by NEC. We don't know anything about this model.** Just we can use it.<br>**NECによって作成されました。このモデルについては何も知りません。** ただし、使用することができます。       |
| cotomi fast v2    | cotomi-Fast V2                                                                        | None        | Internet    | **Made by NEC. We don't know anything about this model.** Just we can use it.<br>**NECによって作成されました。このモデルについては何も知りません。** ただし、使用することができます。       |
| cotomi pro v2     | cotomi-Pro V2                                                                         | None        | Internet    | **Made by NEC. We don't know anything about this model.** Just we can use it.<br>**NECによって作成されました。このモデルについては何も知りません。** ただし、使用することができます。       |
| granite 3 8B      | [granite-3.0-8B-Instruct](https://huggingface.co/ibm-granite/granite-3.0-8b-instruct) | None        | macllm01    | Temporally deploying.<br>一時的に展開中です。                                                                                                                                               |
| Phi 3.5 mini 3.8B | [Phi-3.5-mini](https://huggingface.co/microsoft/Phi-3.5-mini-instruct)                | None        | macllm01    | Temporally deploying.<br>一時的に展開中です。                                                                                                                                               |
| gpt-4o            | ChatGPT-4o                                                                            | None        | Azure       | Resource name: Brain-Verify-EastUS-ots.<br>リソース名: Brain-Verify-EastUS-ots                                                                                                              |

## Update History

<details>
<summary> Click to Open History </summary>

### v1.3.4

- Add explanation for each model in this release-note
- Change Available Models to table

### v1.3.3 (2024-11-07)

- Change chat-history view
    - From now, both side scroll same time
    - It sometimes output answers for same question in different height
    - Currently, we don't need to annoy this issue!
- Add ChatGPT-4o page
- Add Release-note (this)
- Sort pages order

</details>
