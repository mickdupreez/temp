# -*- encoding: utf-8 -*-
# stub: clocale 0.0.4 ruby lib
# stub: ext/clocale/extconf.rb

Gem::Specification.new do |s|
  s.name = "clocale".freeze
  s.version = "0.0.4"

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.require_paths = ["lib".freeze]
  s.authors = ["Claudio Bley".freeze]
  s.date = "2018-08-11"
  s.email = ["claudio.bley@gmail.com".freeze]
  s.extensions = ["ext/clocale/extconf.rb".freeze]
  s.files = ["ext/clocale/extconf.rb".freeze]
  s.homepage = "https://github.com/avdv/clocale".freeze
  s.licenses = ["MIT".freeze]
  s.rubygems_version = "3.1.2".freeze
  s.summary = "A Ruby gem that wraps C locale functions.".freeze

  s.installed_by_version = "3.1.2" if s.respond_to? :installed_by_version

  if s.respond_to? :specification_version then
    s.specification_version = 4
  end

  if s.respond_to? :add_runtime_dependency then
    s.add_development_dependency(%q<codecov>.freeze, ["~> 0.1.10"])
    s.add_development_dependency(%q<rake>.freeze, ["~> 12.3"])
    s.add_development_dependency(%q<rake-compiler>.freeze, ["~> 1.0"])
    s.add_development_dependency(%q<rspec>.freeze, ["~> 3.7"])
    s.add_development_dependency(%q<rubocop>.freeze, ["~> 0.58"])
    s.add_development_dependency(%q<rubocop-rspec>.freeze, ["~> 1.27"])
    s.add_development_dependency(%q<rubygems-tasks>.freeze, ["~> 0.2"])
  else
    s.add_dependency(%q<codecov>.freeze, ["~> 0.1.10"])
    s.add_dependency(%q<rake>.freeze, ["~> 12.3"])
    s.add_dependency(%q<rake-compiler>.freeze, ["~> 1.0"])
    s.add_dependency(%q<rspec>.freeze, ["~> 3.7"])
    s.add_dependency(%q<rubocop>.freeze, ["~> 0.58"])
    s.add_dependency(%q<rubocop-rspec>.freeze, ["~> 1.27"])
    s.add_dependency(%q<rubygems-tasks>.freeze, ["~> 0.2"])
  end
end
