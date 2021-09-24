variable "vm_name_input" {
  type=string
}

provider "google" {
  project = "buoyant-embassy-326120"
  region  = "europe-north1"
  zone    = "europe-north1-a"
}

resource "google_compute_instance" "ass01" {
  name = var.vm_name_input
  machine_type = "f1-micro"

  boot_disk {
   initialize_params {
     image = "debian-cloud/debian-10-buster-v20210817"
   }
}
 network_interface {
   network = "default"
}
}

resource "google_compute_address" "ip_address" {
  name = "ip-ass01"
}

output "vm_name" {
  value = google_compute_instance.ass01.name
}

output "public_ip" {
  value = google_compute_address.ip_address.address
}
