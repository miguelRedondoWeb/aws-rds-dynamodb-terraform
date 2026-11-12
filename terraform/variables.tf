
# Ejercicio 6 - Variables de Terraform

variable "mi_ip_publica" {
  description = "Direccion IPv4 publica autorizada para acceder a MySQL"
  type        = string

  validation {
    condition     = can(cidrhost(var.mi_ip_publica, 0)) && endswith(var.mi_ip_publica, "/32")
    error_message = "Introduce una direccion IPv4 con mascara /32."
  }
}
