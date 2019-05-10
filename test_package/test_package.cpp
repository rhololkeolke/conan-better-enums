// #include <cpprest/json.h>
#include <enum.h>

BETTER_ENUM(Channel, int, Red=1, Green, Blue)

int main()
{
  Channel c = Channel::_from_string("Red");
  const char *s = c._to_string();

  size_t n = Channel::_size();
  for(Channel c : Channel::_values()) {
    // run something
  }

  switch (c) {
  case Channel::Red:
    break;
  case Channel::Green:
    break;
  case Channel::Blue:
    break;
  }


  Channel c2 = Channel::_from_integral(3);

  constexpr Channel c3 = Channel::_from_string("Blue");
}
