# -*- encoding: utf-8 -*-
# stub: colorls 1.2.0 ruby lib

Gem::Specification.new do |s|
  s.name = "colorls".freeze
  s.version = "1.2.0"

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.require_paths = ["lib".freeze]
  s.authors = ["Athitya Kumar".freeze]
  s.bindir = "exe".freeze
  s.date = "2019-04-09"
  s.email = ["athityakumar@gmail.com".freeze]
  s.executables = ["colorls".freeze]
  s.files = ["exe/colorls".freeze]
  s.homepage = "https://github.com/athityakumar/colorls".freeze
  s.licenses = ["MIT".freeze]
  s.post_install_message = "\n  *******************************************************************\n    Changes introduced in colorls\n\n    Sort by dirs  : -sd flag has been renamed to --sd\n    Sort by files : -sf flag has been renamed to --sf\n    Git status    : -gs flag has been renamed to --gs\n\n    Clubbed flags : `colorls -ald` works\n    Help menu     : `colorls -h` provides all possible flag options\n\n    Tab completion enabled for flags\n\n    -t flag : Previously short for --tree, has been re-allocated to sort results by time\n    -r flag : Previously short for --report, has been re-allocated to reverse sort results\n\n    Man pages have been added. Checkout `man colorls`.\n\n  *******************************************************************\n".freeze
  s.required_ruby_version = Gem::Requirement.new(">= 2.3.0".freeze)
  s.rubygems_version = "3.1.2".freeze
  s.summary = "A Ruby CLI gem that beautifies the terminal's ls command, with color and font-awesome icons.".freeze

  s.installed_by_version = "3.1.2" if s.respond_to? :installed_by_version

  if s.respond_to? :specification_version then
    s.specification_version = 4
  end

  if s.respond_to? :add_runtime_dependency then
    s.add_runtime_dependency(%q<clocale>.freeze, ["~> 0"])
    s.add_runtime_dependency(%q<filesize>.freeze, ["~> 0"])
    s.add_runtime_dependency(%q<manpages>.freeze, ["~> 0"])
    s.add_runtime_dependency(%q<rainbow>.freeze, [">= 2.2", "< 4.0"])
    s.add_development_dependency(%q<bundler>.freeze, ["~> 2.0"])
    s.add_development_dependency(%q<codecov>.freeze, ["~> 0.1"])
    s.add_development_dependency(%q<diffy>.freeze, ["~> 3"])
    s.add_development_dependency(%q<rake>.freeze, ["~> 12"])
    s.add_development_dependency(%q<rdoc>.freeze, ["~> 6.1"])
    s.add_development_dependency(%q<ronn>.freeze, ["~> 0"])
    s.add_development_dependency(%q<rspec>.freeze, ["~> 3.7"])
    s.add_development_dependency(%q<rspec-its>.freeze, ["~> 1.2"])
    s.add_development_dependency(%q<rubocop>.freeze, ["~> 0.67.2"])
    s.add_development_dependency(%q<rubocop-performance>.freeze, ["~> 1.1.0"])
    s.add_development_dependency(%q<rubocop-rspec>.freeze, ["~> 1.27"])
    s.add_development_dependency(%q<rubygems-tasks>.freeze, ["~> 0"])
    s.add_development_dependency(%q<simplecov>.freeze, ["~> 0.16.1"])
  else
    s.add_dependency(%q<clocale>.freeze, ["~> 0"])
    s.add_dependency(%q<filesize>.freeze, ["~> 0"])
    s.add_dependency(%q<manpages>.freeze, ["~> 0"])
    s.add_dependency(%q<rainbow>.freeze, [">= 2.2", "< 4.0"])
    s.add_dependency(%q<bundler>.freeze, ["~> 2.0"])
    s.add_dependency(%q<codecov>.freeze, ["~> 0.1"])
    s.add_dependency(%q<diffy>.freeze, ["~> 3"])
    s.add_dependency(%q<rake>.freeze, ["~> 12"])
    s.add_dependency(%q<rdoc>.freeze, ["~> 6.1"])
    s.add_dependency(%q<ronn>.freeze, ["~> 0"])
    s.add_dependency(%q<rspec>.freeze, ["~> 3.7"])
    s.add_dependency(%q<rspec-its>.freeze, ["~> 1.2"])
    s.add_dependency(%q<rubocop>.freeze, ["~> 0.67.2"])
    s.add_dependency(%q<rubocop-performance>.freeze, ["~> 1.1.0"])
    s.add_dependency(%q<rubocop-rspec>.freeze, ["~> 1.27"])
    s.add_dependency(%q<rubygems-tasks>.freeze, ["~> 0"])
    s.add_dependency(%q<simplecov>.freeze, ["~> 0.16.1"])
  end
end
