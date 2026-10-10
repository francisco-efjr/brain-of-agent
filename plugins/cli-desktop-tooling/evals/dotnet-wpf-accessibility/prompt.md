---
name: dotnet-wpf-accessibility
description: Mede se a revisão de um trecho WPF aponta nome acessível ausente em botão só com ícone, cores fixas em alto contraste, handler de clique acessando o repositório e MVVM, tratando Narrator como etapa humana e declarando lacunas de fonte do WPF.
tags: [cli-desktop-tooling, dotnet-desktop-review, desktop, acessibilidade]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: Achados com evidência e correção por item, comandos no lugar de handlers, verificação com Narrator como etapa humana e lacunas declaradas sem afirmar execução.
model: sonnet
---

Meu app de estoque em WPF (.NET 8) precisa funcionar com leitor de tela, o cliente exigiu. Revisa esse trecho do XAML e do code-behind?

MainWindow.xaml:

```xml
<Window x:Class="Estoque.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
  <StackPanel>
    <TextBox x:Name="Busca" />
    <Button Content="&#xE74D;" FontFamily="Segoe MDL2 Assets"
            Click="Apagar_Click"
            Background="#FFEEEEEE" Foreground="#FF999999" />
    <DataGrid x:Name="Itens" AutoGenerateColumns="True" />
  </StackPanel>
</Window>
```

MainWindow.xaml.cs:

```csharp
private void Apagar_Click(object sender, RoutedEventArgs e)
{
    var item = (Produto)Itens.SelectedItem;
    _db.Remove(item);
    _db.SaveChanges();
}
```
