<#
Script  :  Azure-OpenAI-Copilot-Integration-API.ps1
Version :  1.0
Date    :  7/17/2025
Author: Jody Ingram
Notes: This uses Azure OpenAI to connect PowerShell and Copilot/GPT for pushing queries.
#>

# Azure OpenAI Only
function Ask-Copilot {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory=$true, Position=0)]
        [string]$Prompt
    )
 
    $ApiUrl = "https://<your-resource>.openai.azure.com/openai/deployments/<your-deployment>/chat/completions?api-version=2024-02-15-preview" 
    $ApiKey = "Your-Azure-OpenAI-Key"
 
    # Body
    $Body = @{
        messages = @(
            @{ role = "system"; content = "You are a helpful assistant that explains technical issues." },
            @{ role = "user"; content = $Prompt }
        )
        temperature = 0.5
        max_tokens = 512 # Preference
    } | ConvertTo-Json -Depth 3
 
    # Headers 
    $Headers = @{
        "api-key" = $ApiKey
        "Content-Type"  = "application/json"
    }
 
    # Send Request
    try {
        $Response = Invoke-RestMethod -Uri $ApiUrl -Method Post -Headers $Headers -Body $Body
        $Response.choices[0].message.content
    } catch {
        Write-Error "Failed to get response from Copilot API: $_"
    }
}
